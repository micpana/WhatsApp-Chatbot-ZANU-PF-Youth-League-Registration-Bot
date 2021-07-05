from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from imageai.Prediction.Custom import CustomImagePrediction
import os
from twilio.rest import Client
import requests
import shutil
from GoogleNews import GoogleNews

app = Flask(__name__)
app.debug = True

# Twilio stuff
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    num_media = int(request.values.get("NumMedia"))
    msg = resp.message()
    media = request.values.get('MediaUrl0')
    responded = False

    # get sender details
    source = request.values.get('From')
    split_num = str(source).split(':')
    sender_num_with_country_code = split_num[1]

    if 'help' in incoming_msg:
        msg.body("Hi, I'm an AI powered chatbot designed to help diagnose Covid-19 through image recognition of CT scans (example depicted in the image above). I can also provide you with information regarding the virus. \n \n \n1. Send an image if you want me to perform a diagnosis \n \n2. Respond with '1' if you want to receive the latest news on Covid-19 \n\n3. Respond with '2' if you want to get a list of Covid-19 symptoms \n \n4. Respond with '3' if you want information on prevention and wellness. \n\n5. Respond with '4' if you want information on the treatment of Covid-19")
        msg.media('https://lymphoma-action.org.uk/sites/default/files/inline-images/X-ray-resized.png')
        responded = True
    if incoming_msg == '2':
        msg.media('https://www.aljazeera.com/mritems/Images/2020/3/15/a2c5c6e34b1440c9a06222dec9e814f7_7.jpg')
        msg.body("Image source: Aljazeera \nText source: WHO \n \nPeople may be sick with the virus for 1 to 14 days before developing symptoms. The most common symptoms of coronavirus disease (COVID-19) are fever, tiredness, and dry cough. Most people (about 80%) recover from the disease without needing special treatment. More rarely, the disease can be serious and even fatal. Older people, and people with other medical conditions (such as asthma, diabetes, or heart disease), may be more vulnerable to becoming severely ill.\n \n People may experience: \n-cough \n-fever \n-tiredness \n-difficulty breathing (severe cases) \n\n\nIf you develop a fever, cough, and have difficulty breathing, promptly seek medical care. Call in advance and tell your health provider of any recent travel or recent contact with travelers. \n\n Learn more on https://www.who.int/news-room/q-a-detail/q-a-coronaviruses")
        responded = True
    if incoming_msg == '3':
        msg.media('https://storage.googleapis.com/proudcity/sanrafaelca/uploads/2020/03/web-banner-COVID-prevention.jpg')
        msg.body("Image source: City of San Rafael \nText source: WHO \n\nThere’s currently no vaccine to prevent coronavirus disease (COVID-19). \n\nYou can protect yourself and help prevent spreading the virus to others if you: \n\n Do \n-Wash your hands regularly for 20 seconds, with soap and water or alcohol-based hand rub \n-Cover your nose and mouth with a disposable tissue or flexed elbow when you cough or sneeze \n-Avoid close contact (1 meter or 3 feet) with people who are unwell \n-Stay home and self-isolate from others in the household if you feel unwell \n\nDon't \n-Touch your eyes, nose, or mouth if your hands are not clean \n\n\nIf you develop a fever, cough, and have difficulty breathing, promptly seek medical care. Call in advance and tell your health provider of any recent travel or recent contact with travelers. \n\n Learn more on https://www.who.int/news-room/q-a-detail/q-a-coronaviruses")
        responded = True
    if incoming_msg == '4':
        msg.media('https://www.afro.who.int/sites/default/files/Coronavirus%20Social%20media%20cards/Twitter/4.png')
        msg.body("Image source: Daily Journal \nText source: WHO \n\nThere is no specific medicine to prevent or treat coronavirus disease (COVID-19). People may need supportive care to help them breathe. \n\nSelf care \n\nIf you have mild symptoms, stay at home until you’ve recovered. You can relieve your symptoms if you: \n-rest and sleep \n-keep warm \n-drink plenty of liquids \n-use a room humidifier or take a hot shower to help ease a sore throat and cough \n\n\nIf you develop a fever, cough, and have difficulty breathing, promptly seek medical care. Call in advance and tell your health provider of any recent travel or recent contact with travelers. \n\n Learn more on https://www.who.int/news-room/q-a-detail/q-a-coronaviruses")
        responded = True
    if incoming_msg == '1':
        responded = True
        googlenews = GoogleNews()
        googlenews.search('Covid-19')
        news = googlenews.result()
        try:
            msg.body("*Covid-19 Top Stories in Zimbabwe* \n\nType 's' + the article number to read more (e.g s5)\n\n 1. " + news[0].get("title") + "\n\n2. " + news[1].get("title") + "\n\n3. " + news[2].get("title") + "\n\n4. " + news[3].get("title") + "\n\n5. " + news[4].get("title") + "\n\n6. " + news[5].get("title") + "\n\n7. " + news[6].get("title") + "\n\n8. " + news[7].get("title") + "\n\n9. " + news[8].get("title") + "\n\n10. " + news[9].get("title"))
        except IndexError:
            msg.body("A network error has occured while trying to retrieving the news data, please try again.")
        except:
            msg.body("My news provider is not responding, please try again.")
    if 's' in incoming_msg:
        responded = True
        str_arr = str(incoming_msg).split('s')
        num = str_arr[1]
        article_number = int(num) - 1
        googlenews = GoogleNews()
        googlenews.search('Covid-19')
        news = googlenews.result()
        try:
            msg.body("*" + news[article_number].get("title") + "* \n\n\n" + news[article_number].get("desc") + "\n\n" + "To read more, visit: " + news[article_number].get("link"))
        except IndexError:
            msg.body("The article number you've entered is invalid, please check the article number and try again.")
        except:
            msg.body("Something went wrong, please try again. \n\n This could be a netwok issue or something is wrong Google News.")
    #receiving media
    if num_media:
        responded = True
        #save image 
        resource = requests.get(media, stream=True) # Open the url image, set stream to True, this will return the stream content
        imageType = request.values.get('MediaContentType0')
        str_arr = str(imageType).split('/')
        img_ext = '.' + str_arr[1]
        name_arr = str(media).split('/')
        img_name = name_arr[9]

        local_file = open('./received-images/' + img_name + img_ext, 'wb') # Open a local file with wb ( write binary ) permission.
        resource.raw.decode_content = True # Set decode_content value to True, otherwise the downloaded image file's size will be zero
        shutil.copyfileobj(resource.raw, local_file) # Copy the response stream raw data to local image file.
        del resource # Remove the image url response object.
        #prediction
        #initialize image recognition stuff
        execution_path = os.getcwd()
        prediction = CustomImagePrediction()
        prediction.setModelTypeAsResNet()
        prediction.setModelPath("./model/model_ex-036_acc-1.000000.h5")
        prediction.setJsonPath("./model/model_class.json")
        prediction.loadModel(num_objects=2)
        try:
            predictions, probabilities = prediction.predictImage('./received-images/' + img_name + img_ext, result_count=3)
            predictions_array = []
            for eachPrediction, eachProbability in zip(predictions, probabilities):
                # msg.body(eachPrediction + " : " + str(eachProbability) + "%")
                predictions_array.append(eachPrediction + " : " + str(eachProbability)) # add to pred_arr
                print(eachPrediction , " : " , eachProbability)
                print('')
            # send result as whatsapp message
            message = client.messages.create(
                body=predictions_array[0] + '\n' + predictions_array[1],
                from_='whatsapp:+14155238886',
                to='whatsapp:' + sender_num_with_country_code
            )
        except ValueError:
            # msg.body("Sorry, I cannot run a diagnosis using this image file, please try sending an uncompressed image file.")
            message = client.messages.create(
                body='Sorry, I cannot run a diagnosis using this image file, please try sending an uncompressed image file.',
                from_='whatsapp:+14155238886',
                to='whatsapp:' + sender_num_with_country_code
            )
        except:
            # msg.body("Something went wrong, please try again. \n\n This could be a netwok issue or something is wrong with your file.")
            message = client.messages.create(
                body='Something went wrong, please try again. \n\n This could be a netwok issue or something is wrong with your file.',
                from_='whatsapp:+14155238886',
                to='whatsapp:' + sender_num_with_country_code
            )
    if not responded:
        msg.body("Hi, I'm an AI system designed to help diagnose Covid-19 \n \n \n I could not recognise the command you've entered, please type 'help' to get a list of what I can do.")
    return str(resp)

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0')
    # from waitress import serve
    # serve(app, host='0.0.0.0') # use waitress