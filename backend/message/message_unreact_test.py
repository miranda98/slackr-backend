""" Module Based Imports """
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)))

from utility.storage import box, unbox
from utility.errors import ValueError, AccessError
from utility.security import encode, decode
from utility.wrappers import Virtualized

""" Other Imports """

import re, hashlib, time, uuid

""" Implementation """

import pytest

from . import message_unreact

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoxfQ.OkPmkNhvSri6ZFlANW46hzcoEgict64PXjVuEYLTwJk"

@Virtualized
def test_message_unreact_invalid_token():
	box('tokens', [TOKEN])
	box('users', {"1" : { "u_id": 1, "permission_id": 1 }})
	box('channels', {"1" : {'channel_id': 1, 'name': "1st", 'is_public': True, 'all_members': [1], 'owner_members': [1]}})
	box('messages', {'0' : {
		'message_id': 0,
		'channel_id': 1,
		'u_id': 1,
		'message': "hello, world!",
		'time_created': time.asctime(),
		'reacts': {'1' : {'react_id': 1, 'u_ids' : [1]}},
		'is_pinned': False 
	}})
	
	with pytest.raises(AccessError):
		message_unreact.message_unreact("designedtofail", 0, 1)

@Virtualized
def test_message_unreact_no_such_message():
	box('tokens', [TOKEN])
	box('users', {"1" : { "u_id": 1, "permission_id": 1 }})
	box('channels', {"1" : {'channel_id': 1, 'name': "1st", 'is_public': True, 'all_members': [1], 'owner_members': [1]}})
	box('messages', {})
	
	with pytest.raises(ValueError):
		message_unreact.message_unreact(TOKEN, 0, 1)

@Virtualized
def test_message_unreact_not_authorized():
	box('tokens', [TOKEN])
	box('users', {"1" : { "u_id": 1, "permission_id": 3 }})
	box('channels', {"1" : {'channel_id': 1, 'name': "1st", 'is_public': True, 'all_members': [], 'owner_members': []}})
	box('messages', {'0' : {
		'message_id': 0,
		'channel_id': 1,
		'u_id': 1,
		'message': "hello, world!",
		'time_created': time.asctime(),
		'reacts': {'1' : {'react_id': 1, 'u_ids' : [1]}},
		'is_pinned': False
	}})
	
	with pytest.raises(AccessError):
		message_unreact.message_unreact(TOKEN, 0, 1)

@Virtualized
def test_message_unreact_no_such_react_id():
	box('tokens', [TOKEN])
	box('users', {"1" : { "u_id": 1, "permission_id": 1 }})
	box('channels', {"1" : {'channel_id': 1, 'name': "1st", 'is_public': True, 'all_members': [1], 'owner_members': [1]}})
	box('messages', {'0' : {
		'message_id': 0,
		'channel_id': 1,
		'u_id': 3,
		'message': "hello, world!",
		'time_created': time.asctime(),
		'reacts': {'1' : {'react_id': 1, 'u_ids' : [1]}},
		'is_pinned': True
	}})
	
	with pytest.raises(ValueError):
		message_unreact.message_unreact(TOKEN, 0, 5)

@Virtualized
def test_message_unreact_not_reacted():
	box('tokens', [TOKEN])
	box('users', {"1" : { "u_id": 1, "permission_id": 1 }})
	box('channels', {"1" : {'channel_id': 1, 'name': "1st", 'is_public': True, 'all_members': [1], 'owner_members': [1]}})
	box('messages', {'0' : {
		'message_id': 0,
		'channel_id': 1,
		'u_id': 3,
		'message': "hello, world!",
		'time_created': time.asctime(),
		'reacts': {'1' : {'react_id': 1, 'u_ids' : []}},
		'is_pinned': True
	}})
	
	with pytest.raises(ValueError):
		message_unreact.message_unreact(TOKEN, 0, 1)

@Virtualized
def test_message_unreact_success():
	box('tokens', [TOKEN])
	box('users', {"1" : { "u_id": 1, "permission_id": 1 }})
	box('channels', {"1" : {'channel_id': 1, 'name': "1st", 'is_public': True, 'all_members': [1], 'owner_members': [1]}})
	box('messages', {'0' : {
		'message_id': 0,
		'channel_id': 1,
		'u_id': 1,
		'message': "hello, world!",
		'time_created': time.asctime(),
		'reacts': {'1' : {'react_id': 1, 'u_ids' : [1]}},
		'is_pinned': False 
	}})
	
	message_unreact.message_unreact(TOKEN, 0, 1)

	messages = unbox('messages')

	assert 1 not in messages['0']['reacts']['1']['u_ids']