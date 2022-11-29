from datetime import datetime

from schema import Schema, And, Or, Optional

class Contact:
    new = Schema({
        'role': And(str, Or('lead', 'user')),
        Or('external_id', 'email', only_one=True): str,
        Optional('phone'): str,
        Optional('name'): str,
        Optional('avatar'): str,
        Optional('signed_up_at'): datetime,
        Optional('last_seen_at'): datetime,
        Optional('onwer_id'): int,
        Optional('unsubscribed_from_emails'): bool,
        Optional('custom_attributes'): dict
    })