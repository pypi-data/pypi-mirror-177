# Copyright 2020 The Matrix.org Foundation C.I.C.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, Optional, Union

import frozendict

from twisted.test.proto_helpers import MemoryReactor

import synapse.rest.admin
from synapse.api.constants import EventTypes, HistoryVisibility, Membership
from synapse.api.room_versions import RoomVersions
from synapse.appservice import ApplicationService
from synapse.events import FrozenEvent
from synapse.push.bulk_push_rule_evaluator import _flatten_dict
from synapse.push.httppusher import tweaks_for_actions
from synapse.rest import admin
from synapse.rest.client import login, register, room
from synapse.server import HomeServer
from synapse.storage.databases.main.appservice import _make_exclusive_regex
from synapse.synapse_rust.push import PushRuleEvaluator
from synapse.types import JsonDict, UserID
from synapse.util import Clock

from tests import unittest
from tests.test_utils.event_injection import create_event, inject_member_event


class PushRuleEvaluatorTestCase(unittest.TestCase):
    def _get_evaluator(
        self, content: JsonDict, related_events=None
    ) -> PushRuleEvaluator:
        event = FrozenEvent(
            {
                "event_id": "$event_id",
                "type": "m.room.history_visibility",
                "sender": "@user:test",
                "state_key": "",
                "room_id": "#room:test",
                "content": content,
            },
            RoomVersions.V1,
        )
        room_member_count = 0
        sender_power_level = 0
        power_levels: Dict[str, Union[int, Dict[str, int]]] = {}
        return PushRuleEvaluator(
            _flatten_dict(event),
            room_member_count,
            sender_power_level,
            power_levels.get("notifications", {}),
            {} if related_events is None else related_events,
            True,
        )

    def test_display_name(self) -> None:
        """Check for a matching display name in the body of the event."""
        evaluator = self._get_evaluator({"body": "foo bar baz"})

        condition = {
            "kind": "contains_display_name",
        }

        # Blank names are skipped.
        self.assertFalse(evaluator.matches(condition, "@user:test", ""))

        # Check a display name that doesn't match.
        self.assertFalse(evaluator.matches(condition, "@user:test", "not found"))

        # Check a display name which matches.
        self.assertTrue(evaluator.matches(condition, "@user:test", "foo"))

        # A display name that matches, but not a full word does not result in a match.
        self.assertFalse(evaluator.matches(condition, "@user:test", "ba"))

        # A display name should not be interpreted as a regular expression.
        self.assertFalse(evaluator.matches(condition, "@user:test", "ba[rz]"))

        # A display name with spaces should work fine.
        self.assertTrue(evaluator.matches(condition, "@user:test", "foo bar"))

    def _assert_matches(
        self, condition: JsonDict, content: JsonDict, msg: Optional[str] = None
    ) -> None:
        evaluator = self._get_evaluator(content)
        self.assertTrue(evaluator.matches(condition, "@user:test", "display_name"), msg)

    def _assert_not_matches(
        self, condition: JsonDict, content: JsonDict, msg: Optional[str] = None
    ) -> None:
        evaluator = self._get_evaluator(content)
        self.assertFalse(
            evaluator.matches(condition, "@user:test", "display_name"), msg
        )

    def test_event_match_body(self) -> None:
        """Check that event_match conditions on content.body work as expected"""

        # if the key is `content.body`, the pattern matches substrings.

        # non-wildcards should match
        condition = {
            "kind": "event_match",
            "key": "content.body",
            "pattern": "foobaz",
        }
        self._assert_matches(
            condition,
            {"body": "aaa FoobaZ zzz"},
            "patterns should match and be case-insensitive",
        )
        self._assert_not_matches(
            condition,
            {"body": "aa xFoobaZ yy"},
            "pattern should only match at word boundaries",
        )
        self._assert_not_matches(
            condition,
            {"body": "aa foobazx yy"},
            "pattern should only match at word boundaries",
        )

        # wildcards should match
        condition = {
            "kind": "event_match",
            "key": "content.body",
            "pattern": "f?o*baz",
        }

        self._assert_matches(
            condition,
            {"body": "aaa FoobarbaZ zzz"},
            "* should match string and pattern should be case-insensitive",
        )
        self._assert_matches(
            condition, {"body": "aa foobaz yy"}, "* should match 0 characters"
        )
        self._assert_not_matches(
            condition, {"body": "aa fobbaz yy"}, "? should not match 0 characters"
        )
        self._assert_not_matches(
            condition, {"body": "aa fiiobaz yy"}, "? should not match 2 characters"
        )
        self._assert_not_matches(
            condition,
            {"body": "aa xfooxbaz yy"},
            "pattern should only match at word boundaries",
        )
        self._assert_not_matches(
            condition,
            {"body": "aa fooxbazx yy"},
            "pattern should only match at word boundaries",
        )

        # test backslashes
        condition = {
            "kind": "event_match",
            "key": "content.body",
            "pattern": r"f\oobaz",
        }
        self._assert_matches(
            condition,
            {"body": r"F\oobaz"},
            "backslash should match itself",
        )
        condition = {
            "kind": "event_match",
            "key": "content.body",
            "pattern": r"f\?obaz",
        }
        self._assert_matches(
            condition,
            {"body": r"F\oobaz"},
            r"? after \ should match any character",
        )

    def test_event_match_non_body(self) -> None:
        """Check that event_match conditions on other keys work as expected"""

        # if the key is anything other than 'content.body', the pattern must match the
        # whole value.

        # non-wildcards should match
        condition = {
            "kind": "event_match",
            "key": "content.value",
            "pattern": "foobaz",
        }
        self._assert_matches(
            condition,
            {"value": "FoobaZ"},
            "patterns should match and be case-insensitive",
        )
        self._assert_not_matches(
            condition,
            {"value": "xFoobaZ"},
            "pattern should only match at the start/end of the value",
        )
        self._assert_not_matches(
            condition,
            {"value": "FoobaZz"},
            "pattern should only match at the start/end of the value",
        )

        # it should work on frozendicts too
        self._assert_matches(
            condition,
            frozendict.frozendict({"value": "FoobaZ"}),
            "patterns should match on frozendicts",
        )

        # wildcards should match
        condition = {
            "kind": "event_match",
            "key": "content.value",
            "pattern": "f?o*baz",
        }
        self._assert_matches(
            condition,
            {"value": "FoobarbaZ"},
            "* should match string and pattern should be case-insensitive",
        )
        self._assert_matches(
            condition, {"value": "foobaz"}, "* should match 0 characters"
        )
        self._assert_not_matches(
            condition, {"value": "fobbaz"}, "? should not match 0 characters"
        )
        self._assert_not_matches(
            condition, {"value": "fiiobaz"}, "? should not match 2 characters"
        )
        self._assert_not_matches(
            condition,
            {"value": "xfooxbaz"},
            "pattern should only match at the start/end of the value",
        )
        self._assert_not_matches(
            condition,
            {"value": "fooxbazx"},
            "pattern should only match at the start/end of the value",
        )
        self._assert_not_matches(
            condition,
            {"value": "x\nfooxbaz"},
            "pattern should not match after a newline",
        )
        self._assert_not_matches(
            condition,
            {"value": "fooxbaz\nx"},
            "pattern should not match before a newline",
        )

    def test_no_body(self) -> None:
        """Not having a body shouldn't break the evaluator."""
        evaluator = self._get_evaluator({})

        condition = {
            "kind": "contains_display_name",
        }
        self.assertFalse(evaluator.matches(condition, "@user:test", "foo"))

    def test_invalid_body(self) -> None:
        """A non-string body should not break the evaluator."""
        condition = {
            "kind": "contains_display_name",
        }

        for body in (1, True, {"foo": "bar"}):
            evaluator = self._get_evaluator({"body": body})
            self.assertFalse(evaluator.matches(condition, "@user:test", "foo"))

    def test_tweaks_for_actions(self) -> None:
        """
        This tests the behaviour of tweaks_for_actions.
        """

        actions = [
            {"set_tweak": "sound", "value": "default"},
            {"set_tweak": "highlight"},
            "notify",
        ]

        self.assertEqual(
            tweaks_for_actions(actions),
            {"sound": "default", "highlight": True},
        )

    def test_related_event_match(self):
        evaluator = self._get_evaluator(
            {
                "m.relates_to": {
                    "event_id": "$parent_event_id",
                    "key": "😀",
                    "rel_type": "m.annotation",
                    "m.in_reply_to": {
                        "event_id": "$parent_event_id",
                    },
                }
            },
            {
                "m.in_reply_to": {
                    "event_id": "$parent_event_id",
                    "type": "m.room.message",
                    "sender": "@other_user:test",
                    "room_id": "!room:test",
                    "content.msgtype": "m.text",
                    "content.body": "Original message",
                },
                "m.annotation": {
                    "event_id": "$parent_event_id",
                    "type": "m.room.message",
                    "sender": "@other_user:test",
                    "room_id": "!room:test",
                    "content.msgtype": "m.text",
                    "content.body": "Original message",
                },
            },
        )
        self.assertTrue(
            evaluator.matches(
                {
                    "kind": "im.nheko.msc3664.related_event_match",
                    "key": "sender",
                    "rel_type": "m.in_reply_to",
                    "pattern": "@other_user:test",
                },
                "@user:test",
                "display_name",
            )
        )
        self.assertFalse(
            evaluator.matches(
                {
                    "kind": "im.nheko.msc3664.related_event_match",
                    "key": "sender",
                    "rel_type": "m.in_reply_to",
                    "pattern": "@user:test",
                },
                "@other_user:test",
                "display_name",
            )
        )
        self.assertTrue(
            evaluator.matches(
                {
                    "kind": "im.nheko.msc3664.related_event_match",
                    "key": "sender",
                    "rel_type": "m.annotation",
                    "pattern": "@other_user:test",
                },
                "@other_user:test",
                "display_name",
            )
        )
        self.assertFalse(
            evaluator.matches(
                {
                    "kind": "im.nheko.msc3664.related_event_match",
                    "key": "sender",
                    "rel_type": "m.in_reply_to",
                },
                "@user:test",
                "display_name",
            )
        )
        self.assertTrue(
            evaluator.matches(
                {
                    "kind": "im.nheko.msc3664.related_event_match",
                    "rel_type": "m.in_reply_to",
                },
                "@user:test",
                "display_name",
            )
        )
        self.assertFalse(
            evaluator.matches(
                {
                    "kind": "im.nheko.msc3664.related_event_match",
                    "rel_type": "m.replace",
                },
                "@other_user:test",
                "display_name",
            )
        )

    def test_related_event_match_with_fallback(self):
        evaluator = self._get_evaluator(
            {
                "m.relates_to": {
                    "event_id": "$parent_event_id",
                    "key": "😀",
                    "rel_type": "m.thread",
                    "is_falling_back": True,
                    "m.in_reply_to": {
                        "event_id": "$parent_event_id",
                    },
                }
            },
            {
                "m.in_reply_to": {
                    "event_id": "$parent_event_id",
                    "type": "m.room.message",
                    "sender": "@other_user:test",
                    "room_id": "!room:test",
                    "content.msgtype": "m.text",
                    "content.body": "Original message",
                    "im.vector.is_falling_back": "",
                },
                "m.thread": {
                    "event_id": "$parent_event_id",
                    "type": "m.room.message",
                    "sender": "@other_user:test",
                    "room_id": "!room:test",
                    "content.msgtype": "m.text",
                    "content.body": "Original message",
                },
            },
        )
        self.assertTrue(
            evaluator.matches(
                {
                    "kind": "im.nheko.msc3664.related_event_match",
                    "key": "sender",
                    "rel_type": "m.in_reply_to",
                    "pattern": "@other_user:test",
                    "include_fallbacks": True,
                },
                "@user:test",
                "display_name",
            )
        )
        self.assertFalse(
            evaluator.matches(
                {
                    "kind": "im.nheko.msc3664.related_event_match",
                    "key": "sender",
                    "rel_type": "m.in_reply_to",
                    "pattern": "@other_user:test",
                    "include_fallbacks": False,
                },
                "@user:test",
                "display_name",
            )
        )
        self.assertFalse(
            evaluator.matches(
                {
                    "kind": "im.nheko.msc3664.related_event_match",
                    "key": "sender",
                    "rel_type": "m.in_reply_to",
                    "pattern": "@other_user:test",
                },
                "@user:test",
                "display_name",
            )
        )

    def test_related_event_match_no_related_event(self):
        evaluator = self._get_evaluator(
            {"msgtype": "m.text", "body": "Message without related event"}
        )
        self.assertFalse(
            evaluator.matches(
                {
                    "kind": "im.nheko.msc3664.related_event_match",
                    "key": "sender",
                    "rel_type": "m.in_reply_to",
                    "pattern": "@other_user:test",
                },
                "@user:test",
                "display_name",
            )
        )
        self.assertFalse(
            evaluator.matches(
                {
                    "kind": "im.nheko.msc3664.related_event_match",
                    "key": "sender",
                    "rel_type": "m.in_reply_to",
                },
                "@user:test",
                "display_name",
            )
        )
        self.assertFalse(
            evaluator.matches(
                {
                    "kind": "im.nheko.msc3664.related_event_match",
                    "rel_type": "m.in_reply_to",
                },
                "@user:test",
                "display_name",
            )
        )


class TestBulkPushRuleEvaluator(unittest.HomeserverTestCase):
    """Tests for the bulk push rule evaluator"""

    servlets = [
        synapse.rest.admin.register_servlets_for_client_rest_resource,
        login.register_servlets,
        register.register_servlets,
        room.register_servlets,
    ]

    def prepare(self, reactor: MemoryReactor, clock: Clock, homeserver: HomeServer):
        # Define an application service so that we can register appservice users
        self._service_token = "some_token"
        self._service = ApplicationService(
            self._service_token,
            "as1",
            "@as.sender:test",
            namespaces={
                "users": [
                    {"regex": "@_as_.*:test", "exclusive": True},
                    {"regex": "@as.sender:test", "exclusive": True},
                ]
            },
            msc3202_transaction_extensions=True,
        )
        self.hs.get_datastores().main.services_cache = [self._service]
        self.hs.get_datastores().main.exclusive_user_regex = _make_exclusive_regex(
            [self._service]
        )

        self._as_user, _ = self.register_appservice_user(
            "_as_user", self._service_token
        )

        self.evaluator = self.hs.get_bulk_push_rule_evaluator()

    def test_ignore_appservice_users(self) -> None:
        "Test that we don't generate push for appservice users"

        user_id = self.register_user("user", "pass")
        token = self.login("user", "pass")

        room_id = self.helper.create_room_as(user_id, tok=token)
        self.get_success(
            inject_member_event(self.hs, room_id, self._as_user, Membership.JOIN)
        )

        event, context = self.get_success(
            create_event(
                self.hs,
                type=EventTypes.Message,
                room_id=room_id,
                sender=user_id,
                content={"body": "test", "msgtype": "m.text"},
            )
        )

        # Assert the returned push rules do not contain the app service user
        rules = self.get_success(self.evaluator._get_rules_for_event(event))
        self.assertTrue(self._as_user not in rules)

        # Assert that no push actions have been added to the staging table (the
        # sender should not be pushed for the event)
        users_with_push_actions = self.get_success(
            self.hs.get_datastores().main.db_pool.simple_select_onecol(
                table="event_push_actions_staging",
                keyvalues={"event_id": event.event_id},
                retcol="user_id",
                desc="test_ignore_appservice_users",
            )
        )

        self.assertEqual(len(users_with_push_actions), 0)


class BulkPushRuleEvaluatorTestCase(unittest.HomeserverTestCase):
    servlets = [
        admin.register_servlets,
        login.register_servlets,
        room.register_servlets,
    ]

    def prepare(
        self, reactor: MemoryReactor, clock: Clock, homeserver: HomeServer
    ) -> None:
        self.main_store = homeserver.get_datastores().main

        self.user_id1 = self.register_user("user1", "password")
        self.tok1 = self.login(self.user_id1, "password")
        self.user_id2 = self.register_user("user2", "password")
        self.tok2 = self.login(self.user_id2, "password")

        self.room_id = self.helper.create_room_as(tok=self.tok1)

        # We want to test history visibility works correctly.
        self.helper.send_state(
            self.room_id,
            EventTypes.RoomHistoryVisibility,
            {"history_visibility": HistoryVisibility.JOINED},
            tok=self.tok1,
        )

    def get_notif_count(self, user_id: str) -> int:
        return self.get_success(
            self.main_store.db_pool.simple_select_one_onecol(
                table="event_push_actions",
                keyvalues={"user_id": user_id},
                retcol="COALESCE(SUM(notif), 0)",
                desc="get_staging_notif_count",
            )
        )

    def test_plain_message(self) -> None:
        """Test that sending a normal message in a room will trigger a
        notification
        """

        # Have user2 join the room and cle
        self.helper.join(self.room_id, self.user_id2, tok=self.tok2)

        # They start off with no notifications, but get them when messages are
        # sent.
        self.assertEqual(self.get_notif_count(self.user_id2), 0)

        user1 = UserID.from_string(self.user_id1)
        self.create_and_send_event(self.room_id, user1)

        self.assertEqual(self.get_notif_count(self.user_id2), 1)

    def test_delayed_message(self) -> None:
        """Test that a delayed message that was from before a user joined
        doesn't cause a notification for the joined user.
        """
        user1 = UserID.from_string(self.user_id1)

        # Send a message before user2 joins
        event_id1 = self.create_and_send_event(self.room_id, user1)

        # Have user2 join the room
        self.helper.join(self.room_id, self.user_id2, tok=self.tok2)

        # They start off with no notifications
        self.assertEqual(self.get_notif_count(self.user_id2), 0)

        # Send another message that references the event before the join to
        # simulate a "delayed" event
        self.create_and_send_event(self.room_id, user1, prev_event_ids=[event_id1])

        # user2 should not be notified about it, because they can't see it.
        self.assertEqual(self.get_notif_count(self.user_id2), 0)
