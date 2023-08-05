/*
 * Copyright 2021 The Matrix.org Foundation C.I.C.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

CREATE TABLE IF NOT EXISTS sessions(
    session_type TEXT NOT NULL,  -- The unique key for this type of session.
    session_id TEXT NOT NULL,  -- The session ID passed to the client.
    value TEXT NOT NULL, -- A JSON dictionary to persist.
    expiry_time_ms BIGINT NOT NULL,  -- The time this session will expire (epoch time in milliseconds).
    UNIQUE (session_type, session_id)
);
