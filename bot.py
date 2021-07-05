from flask import Flask, request, send_file, send_from_directory
import requests
import os
import shutil
from datetime import datetime
# Twilio imports
from twilio.twiml.messaging_response import MessagingResponse
from imageai.Prediction.Custom import CustomImagePrediction
from twilio.rest import Client
# database items
from database import init_db
from models import Members, Requests

app = Flask(__name__)
app.debug = True

# server data
server_url = 'https://24f3c9c827bb.ngrok.io'

# geo data                
provinces_and_their_districts = {
    'Bulawayo Province': [
        'Bulawayo Central',
        'Bulawayo West',
        'Bulawayo Suburban',
        'Nkulumane'
    ],
    'Harare Province': [
        'Harare Urban',
        'Harare Rural',
        'Chitungwiza',
        'Epworth'
    ],
    'Manicaland Province': [
        'Buhera District',
        'Chimanimani District',
        'Chipinge District',
        'Makoni District',
        'Mutare District',
        'Mutasa District',
        'Nyanga District'
    ],
    'Mashonaland Central Province': [
        'Bindura',
        'Mbire',
        'Guruve',
        'Mount Darwin',
        'Rushinga',
        'Shamva',
        'Mazowe',
        'Muzarabani'
    ],
    'Mashonaland East Province': [
        'Chikomba',
        'Goromonzi',
        'Marondera',
        'Mudzi',
        'Murehwa',
        'Mutoko',
        'Seke',
        'Uzumba-Maramba-Pfungwe',
        'Wedza'
    ],
    'Mashonaland West Province': [
        'Chegutu',
        'Hurungwe',
        'Kariba',
        'Makonde',
        'Mhondoro-Ngezi',
        'Sanyati',
        'Zvimba'
    ],
    'Masvingo Province': [
        'Bikita', 
        'Chivi', 
        'Zaka',
        'Masvingo',
        'Gutu',
        'Mwenezi',
        'Chiredzi'
    ],
    'Matabeleland North Province': [
        'Binga',
        'Bubi',
        'Hwange',
        'Lupane',
        'Nkayi',
        'Tsholotsho',
        'Umguza'
    ],
    'Matabeleland South Province': [
        'Beitbridge',
        'Bulilima',
        'Gwanda',
        'Insiza',
        'Mangwe',
        'Matobo',
        'Umzingwane'
    ],
    'Midlands Province': [
        'Chirumhanzu',
        'Gokwe North',
        'Gokwe South',
        'Gweru',
        'Kwekwe',
        'Mberengwa',
        'Shurugwi',
        'Zvishavane'
    ]
}

@app.route('/bot', methods=['POST'])
def bot():
    # Twilio variables
    account_sid = ''
    auth_token = ''
    phonenumber = ''
    client = Client(account_sid, auth_token)

    # extract request data
    incoming_msg = request.values.get('Body', '').lower()
    num_media = int(request.values.get("NumMedia"))
    # try:
    #     num_media = int(request.values.get("NumMedia"))
    # except TypeError:
    #     num_media = 0

    media = request.values.get('MediaUrl0')

    # get sender details
    source = request.values.get('From')
    split_num = str(source).split(':')
    sender_num_with_country_code = split_num[1]

    # get sender details
    source = request.values.get('From')
    split_num = str(source).split(':')
    sender_num_with_country_code = split_num[1]

    # initialise Twilio response objects
    resp = MessagingResponse()
    msg = resp.message()

    # var for checking if request has been handled or not
    responded = False

    # checking if their are prior requests needing responses
    all_requests = Requests.objects.filter(phonenumber = str(sender_num_with_country_code))
    
    if len(all_requests) != 0: # we do have requests from the phonenumber user
        pending = True
        
        last_request = all_requests[len(all_requests)-1]

        main_root = last_request.main_root
        root_option = last_request.root_option
        user_response = last_request.user_response
        date_of_request = last_request.date_of_request

        # if user has not responded yet and registration is the main root
        if ((main_root == 'register') and (user_response == 'none')):

            # send message asking for next piece of data
            if root_option == 'id_number':
                save_request = True

                response_body = (
                    'What is your firstname?'
                )

                next_root_option = 'firstname'

                # add current income message to last request's response ,(Make first string character a capital letter)
                Requests.objects(id = last_request.id).update(user_response = incoming_msg.upper())

            # send message asking for next piece of data
            if root_option == 'firstname':
                save_request = True
                
                response_body = (
                    'What is your lastname?'
                )

                next_root_option = 'lastname'

                # add current income message to last request's response ,(Make first string character a capital letter)
                Requests.objects(id = last_request.id).update(user_response = incoming_msg.capitalize())

            if root_option == 'lastname':
                save_request = True
                
                response_body = (
                    "What's your home address?"
                )

                next_root_option = 'home_address'
                
                # add current income message to last request's response ,(Make first string character a capital letter)
                Requests.objects(id = last_request.id).update(user_response = incoming_msg.capitalize())

            if root_option == 'home_address':
                save_request = True
                
                response_body = (
                    'What Province do you reside in?\n\n'
                    '1. Bulawayo Province\n'
                	'2. Harare Province\n'
                	'3. Manicaland Province\n'
                	'4. Mashonaland Central Province\n'
                	'5. Mashonaland East Province\n'
                	'6. Mashonaland West Province\n'
                	'7. Masvingo Province\n'
                	'8. Matabeleland North Province\n'
                	'9. Matabeleland South Province\n'
                	'10. Midlands Province\n'
                )

                next_root_option = 'province'
                
                # add current income message to last request's response ,(Make first string character a capital letter)
                Requests.objects(id = last_request.id).update(user_response = incoming_msg.upper())
            
            if root_option == 'province':
                save_request = True

                provinces = list(provinces_and_their_districts)

                province = provinces[int(incoming_msg)-1] # list indexes start at 0 while user options start at 1

                districts = provinces_and_their_districts[province]

                response_body = (
                    "What's your District?\n\n"
                )

                option_number = 1
                for item in districts:
                    option_string = str(option_number) + '. ' + item + '\n'
                    response_body = response_body + option_string
                    option_number = option_number + 1

                next_root_option = 'district'

                # add current income message to last request's response ,(Make first string character a capital letter)
                Requests.objects(id = last_request.id).update(user_response = province)
            

            if root_option == 'district':
                save_request = True

                province = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'province')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'province'))-1].user_response
                
                districts = provinces_and_their_districts[province]
                district = districts[int(incoming_msg)-1] 

                response_body = (
                    'What is your Polling Station?'
                )

                next_root_option = 'polling_station'

                # add current income message to last request's response ,(Make first string character a capital letter)
                Requests.objects(id = last_request.id).update(user_response = district.capitalize())

            
            if root_option == 'polling_station':
                save_request = True
                
                response_body = (
                    'What is your current branch?'
                )

                next_root_option = 'branch'

                # add current income message to last request's response ,(Make first string character a capital letter)
                Requests.objects(id = last_request.id).update(user_response = incoming_msg.capitalize())


            if root_option == 'branch':
                save_request = True
                
                response_body = (
                    'Select Your Membership\n\n'
                    '1. Youth League\n'
                    '2. Main Wing\n'
                    '3. Women League\n'
                )

                next_root_option = 'membership'

                # add current income message to last request's response ,(Make first string character a capital letter)
                Requests.objects(id = last_request.id).update(user_response = incoming_msg.capitalize())

            
            if root_option == 'membership':
                save_request = True

                if incoming_msg == '1':
                    membership = 'Youth League'
                if incoming_msg == '2':
                    membership = 'Main Wing'
                if incoming_msg == '3':
                    membership = 'Women League'
                
                response_body = (
                    'Want to upload your profile picture?\n\n'
                    '1. Yes\n'
                    '2. No\n'
                )

                next_root_option = 'profile_image'

                # add current income message to last request's response ,(Make first string character a capital letter)
                Requests.objects(id = last_request.id).update(user_response = membership)
            
            if root_option == 'profile_image':
                if incoming_msg == '1':
                    save_request = True
                
                    response_body = (
                        'Send us your selfie.'
                    )

                    next_root_option = 'send_image'

                    response = 'Yes'

                    # add current income message to last request's response ,(Make first string character a capital letter)
                    Requests.objects(id = last_request.id).update(user_response = response)

                if incoming_msg == '2':
                    save_request = False
                    response_body = (
                        'Congratulations {}. You have completed the registration process successfully.\n\n'
                        'To view your profile, respond with *3*'
                    ).format(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'firstname')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'firstname'))-1].user_response)

                    response = 'No'

                    # add current income message to last request's response ,(Make first string character a capital letter)
                    Requests.objects(id = last_request.id).update(user_response = response)

                    # save user data
                    user_data = Members(
                        national_id_number = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'id_number')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'id_number'))-1].user_response,
                        firstname = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'firstname')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'firstname'))-1].user_response,
                        lastname = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'lastname')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'lastname'))-1].user_response,
                        phonenumber = str(sender_num_with_country_code),
                        home_address = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'home_address')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'home_address'))-1].user_response,
                        province = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'province')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'province'))-1].user_response,
                        district = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'district')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'district'))-1].user_response,
                        polling_station = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'polling_station')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'polling_station'))-1].user_response,
                        branch = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'branch')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'branch'))-1].user_response,
                        membership = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'membership')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'membership'))-1].user_response,
                        profile_image = 'none',
                        date_of_registration = str(datetime.now())
                    )
                    user_data.save()
            
            if root_option == 'send_image':
                if num_media: # if message contains media
                    save_request = False
                    response_body = (
                        'Congratulations {}. You have completed the registration process successfully.\n\n'
                        'To view your profile, respond with *3*'
                    ).format(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'firstname')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'firstname'))-1].user_response)

                    # get image resource
                    resource = requests.get(media, stream=True) # Open the url image, set stream to True, this will return the stream content
                    
                    # get the name and extension
                    imageType = request.values.get('MediaContentType0')
                    str_arr = str(imageType).split('/')
                    img_ext = '.' + str_arr[1]
                    name_arr = str(media).split('/')
                    img_name = name_arr[9]

                    # save image
                    local_file = open('./profile-images/' + img_name + img_ext, 'wb') # Open a local file with wb ( write binary ) permission.
                    resource.raw.decode_content = True # Set decode_content value to True, otherwise the downloaded image file's size will be zero
                    shutil.copyfileobj(resource.raw, local_file) # Copy the response stream raw data to local image file.
                    del resource # Remove the image url response object.

                    # add current income message to last request's response ,(Make first string character a capital letter)
                    Requests.objects(id = last_request.id).update(user_response = img_name+img_ext)

                    # save user data
                    user_data = Members(
                        national_id_number = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'id_number')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'id_number'))-1].user_response,
                        firstname = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'firstname')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'firstname'))-1].user_response,
                        lastname = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'lastname')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'lastname'))-1].user_response,
                        phonenumber = str(sender_num_with_country_code),
                        home_address = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'home_address')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'home_address'))-1].user_response,
                        province = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'province')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'province'))-1].user_response,
                        district = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'district')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'district'))-1].user_response,
                        polling_station = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'polling_station')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'polling_station'))-1].user_response,
                        branch = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'branch')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'branch'))-1].user_response,
                        membership = Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'membership')[len(Requests.objects.filter(phonenumber = str(sender_num_with_country_code), root_option = 'membership'))-1].user_response,
                        profile_image = img_name+img_ext,
                        date_of_registration = str(datetime.now())
                    )
                    user_data.save()
                
                else: # if user didn't send media
                    save_request = False
                    response_body = (
                        'Send us your selfie.'
                    )


            # respond to message
            message = client.messages.create(
                body=response_body,
                from_='whatsapp:' + phonenumber,
                to='whatsapp:' + sender_num_with_country_code
            )

            # save request details
            if save_request == True:
                request_details = Requests(
                    phonenumber = str(sender_num_with_country_code),
                    main_root = main_root,
                    root_option = next_root_option,
                    user_response = 'none',
                    date_of_request = str(datetime.now())
                )

                request_details.save()

            responded = True

        else: # no messages in need of a response
            pending = False
    
    else: # user hasn't made requests yet
        pending = False

    if pending == False: # if theres no message in need of a response

        if ((incoming_msg == 'hie') or (incoming_msg == 'join') or (incoming_msg == 'pfee') or (incoming_msg == 'help')): # trigger messages
            response_body = (
                'Hi there! Thank you for using our ZANU YEDU on WhatsApp. Are you ready to get started with YEDU? Press *1*\n'
                'By proceeding with registration, you are agreeing with our T&Cs.\n\n\n'
                '*Explore other options:*\n'
                '2. About\n'
                '3. Profile\n'
            )

            message = client.messages.create(
                media_url=['https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_ZANU-PF.svg/800px-Flag_of_ZANU-PF.svg.png'],
                body=response_body,
                from_='whatsapp:' + phonenumber,
                to='whatsapp:' + sender_num_with_country_code
            )

            # save request details
            request_details = Requests(
                phonenumber = str(sender_num_with_country_code),
                main_root = 'trigger',
                root_option = 'none',
                user_response = 'none',
                date_of_request = str(datetime.now())
            )

            request_details.save()

            responded = True

        if incoming_msg == '1': # register
            # check if user is already registered, do a query using the sender's phonenumber
            members = Members.objects.filter(phonenumber = str(sender_num_with_country_code))

            if len(members) == 0: # user isn't registered
                response_body = (
                    "What is your National ID Number?"
                )

                message = client.messages.create(
                    body=response_body,
                    from_='whatsapp:' + phonenumber,
                    to='whatsapp:' + sender_num_with_country_code
                )

                # save request details
                request_details = Requests(
                    phonenumber = str(sender_num_with_country_code),
                    main_root = 'register',
                    root_option = 'id_number',
                    user_response = 'none',
                    date_of_request = str(datetime.now())
                )

                request_details.save()

                responded = True

            else: # user is already registered
                response_body = (
                    'Hi {}, you have already registered with us.'
                ).format(members[0].firstname)

                message = client.messages.create(
                    body=response_body,
                    from_='whatsapp:' + phonenumber,
                    to='whatsapp:' + sender_num_with_country_code
                )

                # save request details
                request_details = Requests(
                    phonenumber = str(sender_num_with_country_code),
                    main_root = 'register',
                    root_option = 'none',
                    user_response = 'not needed',
                    date_of_request = str(datetime.now())
                )

                request_details.save()

                responded = True
        
        if incoming_msg == '2': # about
            response_body = (
                "Zimbabwe African National Union- Patriotic Front (Zanu PF) is a total Political, Indigenous Economic Emancipation and "
                "a National Liberation Movement Package for Zimbabweans by Zimbabweans prepared to shed their blood in defence of their " 
                "Sovereignty at all times. Its a liberation movement which thrives on and cherishes National Unity which has created the "
                "sound condition of Peace and Security which Zimbabwe has enjoyed and a rare gift many countries dream of. Is driven by "
                "its Democratic African Values where the leadership is accountable to the membership which elected it, hence the holding "
                "of District Conferences, the Annual People’s Conference and the National People’s Congress."
            )

            message = client.messages.create(
                media_url=['https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_ZANU-PF.svg/800px-Flag_of_ZANU-PF.svg.png'],
                body=response_body,
                from_='whatsapp:' + phonenumber,
                to='whatsapp:' + sender_num_with_country_code
            )

            # save request details
            request_details = Requests(
                phonenumber = str(sender_num_with_country_code),
                main_root = 'about',
                root_option = 'none',
                user_response = 'none',
                date_of_request = str(datetime.now())
            )

            request_details.save()

            responded = True

        if incoming_msg == '3': # profile
            # check if user is already registered, do a query using the sender's phonenumber
            members = Members.objects.filter(phonenumber = str(sender_num_with_country_code))
            if len(members) == 0: # shows number has not been used to register yet
                response_body = (
                    'Hello there, please note that you need to be a registered member inorder to have a profile you can view.\n\n'
                    'Respond with *1* to register.'
                )

                message = client.messages.create(
                    media_url=['https://pbs.twimg.com/media/EW63EfWX0AAx4vn.jpg'],
                    body=response_body,
                    from_='whatsapp:' + phonenumber,
                    to='whatsapp:' + sender_num_with_country_code
                )

                # save request details
                request_details = Requests(
                    phonenumber = str(sender_num_with_country_code),
                    main_root = 'profile',
                    root_option = 'none',
                    user_response = 'none',
                    date_of_request = str(datetime.now())
                )

                request_details.save()

                responded = True
            
            else: # if the number is already linked to a registered member
                member = members[0]
                national_id_number = member.national_id_number
                firstname = member.firstname
                lastname = member.lastname
                phone_number = member.phonenumber
                home_address = member.home_address
                province = member.province
                district = member.district
                polling_station = member.polling_station
                branch = member.branch
                membership = member.membership
                profile_image = member.profile_image
                date_of_registration = member.date_of_registration

                response_body = (
                    '*Your Profile*\n\n'
                    'Firstname: \n{}\n\n'
                    'Lastname: \n{}\n\n'
                    'National ID Number: \n{}\n\n'
                    'Phonenumber: \n{}\n\n'
                    'Home Address: \n{}\n\n'
                    'Province: \n{}\n\n'
                    'District: \n{}\n\n'
                    'Polling Station: \n{}\n\n'
                    'Branch: \n{}\n\n'
                    'Youth League: \n{}\n\n'
                    'Date Of Registration: \n{}\n\n'
                ).format(firstname, lastname, national_id_number, phone_number, home_address, province, district, polling_station, branch, membership, date_of_registration[0:16])
                
                image_url = server_url + '/media/' + profile_image

                message = client.messages.create(
                    media_url=[image_url],
                    body=response_body,
                    from_='whatsapp:' + phonenumber,
                    to='whatsapp:' + sender_num_with_country_code
                )

                # save request details
                request_details = Requests(
                    phonenumber = str(sender_num_with_country_code),
                    main_root = 'profile',
                    root_option = 'none',
                    user_response = 'none',
                    date_of_request = str(datetime.now())
                )

                request_details.save()

                responded = True

        if responded == False: # incoming message wasn't recognised
            response_body = (
                'Hi there. I could not recognise your message.\n\n'
                'Please respond with a *Hie* to get started.\n'
            )

            message = client.messages.create(
                body=response_body,
                from_='whatsapp:' + phonenumber,
                to='whatsapp:' + sender_num_with_country_code
            )

            # save request details
            request_details = Requests(
                phonenumber = str(sender_num_with_country_code),
                main_root = 'unknown',
                root_option = 'none',
                user_response = 'none',
                date_of_request = str(datetime.now())
            )

            request_details.save()

    # Twilio POST function return data
    return str(resp)

@app.route('/media/<filename>', methods=['GET', 'POST'])
def media(filename):
    from pathlib import Path

    root = Path('.')

    folder_path = root / 'profile-images'

    return send_from_directory(folder_path, filename, as_attachment=True)

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0')
    # from waitress import serve
    # serve(app, host='0.0.0.0') # use waitress