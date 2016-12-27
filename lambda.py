"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def build_audio_response(title, begin_output, audio_url, end_output, reprompt_text, should_end_session = False):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': '<speak>' + begin_output + '<audio src="' + audio_url + '"/>' + end_output + '</speak>'
            },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': begin_output + end_output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Musician's Assistant. " \
                    "Ask for a note by saying, " \
                    "play an A"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Ask for a note by saying, " \
                    "play an A"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def play_note(intent, session):
    card_title = intent['name']
    session_attributes = {}

    if 'Note' in intent['slots']:
        note_to_play = intent['slots']['Note']['value']
        output_note = get_note_url(note_to_play)
    
    title = "Note playing."
    begin_output = "Here is your note. "
    audio_url = output_note
    end_output = ""
    reprompt_text = None
    should_end_session = True

    return build_response(session_attributes, build_audio_response(
        title,  begin_output, audio_url, end_output, reprompt_text, should_end_session))

def get_note_url(note_to_play):
    if note_to_play == "a" or note_to_play == "egg":
        return note_a()
    elif note_to_play == "d" or note_to_play == "die":
        return note_d()
    elif note_to_play == "g" or note_to_play == "ge" or note_to_play == "jean":
        return note_g()
    elif note_to_play == "e" or note_to_play == "need" or note_to_play == "and i" or note_to_play == "I":
        return note_e()
    else:
        raise ValueError('Invalid note, "'+ note_to_play +'"')



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "PlayNoteIntent":
        return play_note(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

#----------------Audio files
def note_a():
    return "https://s3.amazonaws.com/musiciansassistant/a_440.mp3"
def note_d():
    return "https://s3.amazonaws.com/musiciansassistant/d_293_7.mp3"
def note_g():
    return "https://s3.amazonaws.com/musiciansassistant/g_196.mp3"
def note_e():
    return "https://s3.amazonaws.com/musiciansassistant/e_659_3.mp3"


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
