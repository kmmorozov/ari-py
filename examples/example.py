#!/usr/bin/env python

"""Brief example of using the channel API.

This app will answer any channel sent to Stasis(hello), and play "Hello,
world" to the channel. For any DTMF events received, the number is played back
to the channel. Press # to hang up, and * for a special message.
"""

#
# Copyright (c) 2013, Digium, Inc.
#

import ari

client = ari.connect('http://localhost:8088/', 'hey', 'peekaboo!')


def on_dtmf(channel, event):

    digit = event['digit']
    if digit == '#':
        channel.play(media='sound:goodbye')
        channel.continueInDialplan()
    elif digit == '*':
        channel.play(media='sound:asterisk-friend')
    else:
        channel.play(media='sound:digits/%s' % digit)


def on_start(channel, event):
    channel.on_event('ChannelDtmfReceived', on_dtmf)
    channel.answer()
    channel.play(media='sound:hello-world')


client.on_channel_event('StasisStart', on_start)

# Run the WebSocket
client.run(apps="hello!")
