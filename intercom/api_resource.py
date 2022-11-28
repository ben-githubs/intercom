from dataclasses import MISSING, dataclass, field
from datetime import datetime
from typing import List, Union

class Resource:
    def __init__(self, client):
        self.client = client

def unix_to_datetime(obj, *args):
    # Convert UNIX timestamp to Python datetime
    for attr in args:
        val = getattr(obj, attr)
        if val: # Don't try to make datetime from None
            setattr(obj, attr, datetime.utcfromtimestamp(val))


class CursorList:
    def __init__(self, client, endpoint, data: list, total_count: int, pages: dict):
        self.client = client
        self.url = endpoint
        self.length = total_count
        self.starting_after = pages.get('next', dict()).get('starting_after')
        self.items = data

    def __next_page(self):
        if self.starting_after:
            new_list = self.client.get(f"{self.url}?starting_after={self.starting_after}")
            self.starting_after = new_list.starting_after
            self.items += new_list.items
    
    def __len__(self):
        return self.length
    
    def __iter__(self):
        self.n = 0
        return self
    
    def __next__(self):
        if self.n < self.length:
            if self.n == len(self.items):
                self.__next_page()
            self.n += 1
            return self.items[self.n-1]
        else:
            raise StopIteration
    

class PagedList:
    def __init__(self, client, data: list, total_count: int, pages: dict):
        self.client = client
        self.length = total_count
        self.next = ''
        if pages.get('next'):
            self.next = pages['next'].replace(client.host, '')
        self.items = data

    def __next_page(self):
        if self.next:
            new_list = self.client.get(self.next)
            self.next = new_list.next
            self.items += new_list.items
    
    def __len__(self):
        return self.length
    
    def __iter__(self):
        self.n = 0
        return self
    
    def __next__(self):
        if self.n < self.length:
            if self.n == len(self.items):
                self.__next_page()
            self.n += 1
            return self.items[self.n-1]
        else:
            raise StopIteration

"""
    Level 1 Objects - No dependence on any others
"""

@dataclass
class Admin(Resource):
    __api_type__ = 'admin'
    client: object
    id: str
    name: str
    email: str
    away_mode_enabled: bool
    away_mode_reassign: bool
    has_inbox_seat: bool
    team_ids: List[str]
    job_title: str = ''
    avatar: str = ''

    def set_away(self, away, reassign=False):
        """ Sets the Intercom away status of this Admin.
            away (bool): whether or not the admin is away
            reassign (bool): should new replies to their convos be reassigned?
        """
        data = {
            'away_mode_enabled': away,
            'away_mode_reassign': reassign
        }
        self.client.put(f"admins/{self.id}/away", body=data)

@dataclass
class AddressableList:
    __api_type__ = 'list'
    client: object
    url: str
    total_count: int
    has_more: bool
    data: list

@dataclass
class Bot(Resource):
    __api_type__ = 'bot'
    client: object
    id: str
    name: str
    email: str

@dataclass
class Segment(Resource):
    __api_type__ = 'segment'
    client: object
    id: str
    name: str
    created_at: datetime = MISSING
    updated_at: datetime = MISSING
    person_type: str = MISSING
    count: int = MISSING

@dataclass
class Statistics(Resource):
    __api_type__ = 'conversation_statistics'
    client: object
    time_to_assignment: int
    time_to_admin_reply: int
    time_to_first_close: int
    time_to_last_close: int
    median_time_to_close: int
    first_contact_reply_at: datetime
    first_assignment_at: datetime
    first_admin_reply_at: datetime
    first_close_at: datetime
    last_assignment_at: datetime
    last_assignment_admin_reply_at: datetime
    last_contact_reply_at: datetime
    last_admin_reply_at: datetime
    last_close_at: datetime
    last_closed_by_id: int # The docs say this is last_closed_by: dict, but I get this when I query
    count_reopens: int
    count_assignments: int
    count_conversation_parts: int

    def __post_init__(self):
        # Convert UNIX timestamp to Python datetime
        unix_to_datetime(self, 'first_contact_reply_at', 'first_assignment_at', 
            'first_admin_reply_at', 'first_close_at', 'last_assignment_at',
            'last_assignment_admin_reply_at', 'last_contact_reply_at', 'last_admin_reply_at',
            'last_close_at')

@dataclass
class Location(Resource):
    __api_type__ = 'location'
    client: object
    country: str
    country_code: str
    continent_code: str
    region: str
    city: str

@dataclass
class Plan(Resource):
    __api_type__ = 'plan'
    client: object
    id: str
    name: str

@dataclass
class SLASummary(Resource):
    __api_type__ = 'conversation_sla_summary'
    client: object
    sla_name: str
    sla_status: str

@dataclass
class SocialProfile(Resource):
    __api_type__ = 'social_profile'
    client: object
    name: str
    url: str

@dataclass
class Tag(Resource):
    __api_type__ = 'tag'
    client: object
    id: str
    name: str

@dataclass
class Team(Resource):
    __api_type__ = 'team'
    client: object
    id: str
    name: str
    admin_ids: List[str]

@dataclass
class User(Resource):
    __api_type__ = 'user'
    client: object
    id: str
    name: str
    email: str

"""
    Level 2 Objects - Depends only on level 1
"""

@dataclass
class Company(Resource):
    __api_type__ = 'company'
    client: object
    id: str
    company_id: str = ''
    app_id: str = ''
    name: str = ''
    created_at: datetime = None
    remote_created_at: datetime = None
    updated_at: datetime = None
    last_request_at: datetime = None
    custom_attributes: dict = field(default_factory=dict)
    session_count: int = -1
    monthly_spend: int = -1
    user_count: int = -1
    tags: List[Tag] = field(default_factory=list)
    segments: List[Segment] = field(default_factory=list)
    plan: Plan = None
    size: int = -1
    website: str = ''
    url: str = ''
    industry: str = ''

    def __post_init__(self):
        # Convert UNIX timestamp to Python datetime
        unix_to_datetime(self, 'created_at', 'remote_created_at', 'updated_at', 'last_request_at')

@dataclass
class Contact(Resource):
    __api_type__ = 'contact'
    client: object
    id: str
    workspace_id: str = field(default=MISSING)
    external_id: str = field(default=MISSING)
    role: str = field(default=MISSING)
    email: str = field(default=MISSING)
    phone: str = field(default=MISSING)
    name: str = field(default=MISSING)
    avatar: str = field(default=MISSING)
    owner_id: int = field(default=MISSING)
    social_profiles: List[SocialProfile] = field(default=MISSING)
    has_hard_bounced: bool = field(default=MISSING)
    marked_email_as_spam: bool = field(default=MISSING)
    unsubscribed_from_emails: bool = field(default=MISSING)
    created_at: datetime = field(default=MISSING)
    updated_at: datetime = field(default=MISSING)
    signed_up_at: datetime = field(default=MISSING)
    last_seen_at: datetime = field(default=MISSING)
    last_replied_at: datetime = field(default=MISSING)
    last_contacted_at: datetime = field(default=MISSING)
    last_email_opened_at: datetime = field(default=MISSING)
    last_email_clicked_at: datetime = field(default=MISSING)
    language_override: str = field(default=MISSING)
    browser: str = field(default=MISSING)
    browser_version: str = field(default=MISSING)
    browser_language: str = field(default=MISSING)
    os: str = field(default=MISSING)
    location: str = field(default=MISSING)
    android_app_name: str = field(default=MISSING)
    android_app_version: str = field(default=MISSING)
    android_device: str = field(default=MISSING)
    android_os_version: str = field(default=MISSING)
    android_sdk_version: str = field(default=MISSING)
    android_last_seen_at: datetime = field(default=MISSING)
    ios_app_name: str = field(default=MISSING)
    ios_app_version: str = field(default=MISSING)
    ios_device: str = field(default=MISSING)
    ios_os_version: str = field(default=MISSING)
    ios_sdk_version: str = field(default=MISSING)
    ios_last_seen_at: datetime = field(default=MISSING)
    custom_attributes: dict = field(default=MISSING)
    tags: AddressableList = field(default=MISSING)
    notes: AddressableList = field(default=MISSING)
    companies: AddressableList = field(default=MISSING)
    opted_in_subscription_types: AddressableList = field(default=MISSING)
    opted_out_subscription_types: AddressableList = field(default=MISSING)
    utm_campaign: object = field(default=MISSING) # No idea what these utm fields are, not in docs
    utm_content: object = field(default=MISSING)
    utm_medium: object = field(default=MISSING)
    utm_source: object = field(default=MISSING)
    utm_term: object = field(default=MISSING)
    referrer: str = field(default=MISSING)
    sms_consent: bool = field(default=MISSING)
    unsubscribed_from_sms: bool = field(default=MISSING)

    def __post_init__(self):
        # Convert UNIX timestamp to Python datetime
        unix_to_datetime(self, 'created_at', 'updated_at', 'signed_up_at', 'last_seen_at',
            'last_replied_at', 'last_contacted_at', 'last_email_opened_at',
            'last_email_clicked_at', 'android_last_seen_at', 'ios_last_seen_at')

@dataclass
class ConversationPart(Resource):
    __api_type__ = 'conversation_part'
    client: object
    id: str
    part_type: str
    body: str
    created_at: datetime
    updated_at: datetime
    notified_at: datetime
    assigned_to: str
    author: Union[Bot, Admin, User]
    attachments: list
    redacted: bool

    def __post_init__(self):
        unix_to_datetime(self, 'created_at', 'updated_at', 'notified_at')

@dataclass
class Source(Resource):
    client: object
    id: str
    delivered_as: str
    subject: str
    author: Union[Contact, Admin, Team]
    attachments: list
    url: str
    redacted: bool

"""
    Level 3
"""

@dataclass
class Conversation(Resource):
    __api_type__ = 'conversation'
    client: object
    id: str
    created_at: datetime
    updated_at: datetime
    source: Source
    contacts: List[str] # I'll only store ids
    teammates: List[str] # I'll only store ids
    title: str
    admin_assignee_id: int
    team_assinee_id: int
    custom_attributes: dict
    open: bool
    state: str
    read: bool
    waiting_since: datetime
    snoozed_until: datetime
    tags: List[Tag]
    first_contact_reply: dict
    priority: bool # return priority == "priority"
    sla_applied: SLASummary
    conversation_rating: dict
    statistics: Statistics
    conversation_parts: List[ConversationPart]

    def __post_init__(self):
        # Convert UNIX timestamp to Python datetime
        unix_to_datetime('created_at', 'updated_at', 'waiting_since', 'snoozed_until')


def object_hook(data: dict, client=None):
    """ 'data' is a dictionary produced by the json deserialization. In this dictionary, Intercom 
    probably added a 'type' key. Using that, we can convert some of the dictionaries into actual
    objects.
    """
    obj_type = data.pop('type', None)
    if obj_type is None:
        return data
    mapping = {
        'admin': Admin,
        'contact': Contact,
        'company': Company,
        'email': Source,
        'facebook': Source,
        'location': Location,
        'plan': Plan,
        'push': Source,
        'social_profile': SocialProfile,
        'team': Team,
        'twitter': Source,
    }

    if obj_type in mapping:
        #TODO: Find a better way to add client to the Resource
        obj = mapping[obj_type](client, **data)
        return obj
    
    if obj_type == 'conversation':
        # There's two possibilities: this is a conversation or a source obj. FML
        if 'delivered_as' in data:
            return Source(client, **data)
        else:
            return Conversation(client, **data)

    if obj_type == 'list':
        # Check pagination
        if 'pages' in data and isinstance(data['pages'].get('next'), str):
            data['data'] = PagedList(client, data['data'], data['total_count'], data['pages'])
        elif 'pages' in data and 'next' in data['pages'] and 'starting_after' in data['pages'].get('next'):
            data['data'] = CursorList(client, 'contacts', data['data'], data['total_count'], data['pages'])


        # There's 2 types of list: regular lists and AddressableLists. We need to handle both.
        if 'url' in data: # Returns true for AddressableList
            return AddressableList(**data)
        else:
            return data.get('data', [])
    if obj_type.endswith('.list'):
        # These suck, because sometimes you can get 'admin.list' or 'contact.list', but the
        # data is stored under 'admins' or 'contacts'
        key = obj_type.split('.')[0]
        # Here we do the pluralization. Companties is the only special case resource.
        if key == 'company':
            key = 'companies'
        else:
            key += 's'
        return data.get(key)
    
    # Return dictionary if none of the above fit
    if obj_type:
        data['type'] = obj_type
    return data
    