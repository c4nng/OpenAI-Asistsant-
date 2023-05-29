import speech_recognition as sr
import pyttsx3
import openai
import configparser

config = configparser.ConfigParser()
config.read('config.ini') #Config.ini (Please specify the file path
# config.ini (Open AI Api key)
openai.api_key = config.get('API','openai_api_key')
# G ❤
def get_openai_response(question):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=question,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Türkçe sesi seçin (örneğin: Türkiye Türkçesi için 0. index)
    turkish_voice_id = 0
    engine.setProperty('voice', voices[turkish_voice_id].id)
    
    engine.setProperty('rate', 150)  # Konuşma hızı
    engine.setProperty('volume', 1)  # Ses seviyesi (0.0 ile 1.0 arasında)
    engine.say(text)
    engine.runAndWait()

#Keyword
listen_keyword = "beni dinle" #run
exit_keyword = "çıkış" #exit

# Mikrofon nesnesini oluşturun
r = sr.Recognizer()

# Ses kaynağı olarak varsayılan mikrofonu kullanın
mic = sr.Microphone()

while True:
    # Kullanıcıdan sesli giriş alın
    with mic as source:
        print("Lütfen bir şeyler söyleyin:")
        audio = r.listen(source)

    # Sesli girişi metne dönüştürün
    try:
        user_input = r.recognize_google(audio, language='tr-TR')
        print("Siz: ", user_input)
    except sr.UnknownValueError:
        print("Ses anlaşılamadı")
        continue

    # Anahtar kelimeyi kontrol edin ve programı etkinleştirin
    if listen_keyword in user_input:
        print("Program etkinleştirildi. Sorularınızı sorabilirsiniz.")
        while True:
            # Kullanıcıdan soruyu sesli olarak alın
            with mic as source:
                print("Sorunuzu sesli olarak sorun:")
                audio = r.listen(source)

            # Sesli girişi metne dönüştürün
            try:
                user_question = r.recognize_google(audio, language='tr-TR')
                print("Sorunuz: ", user_question)
            except sr.UnknownValueError:
                print("Ses anlaşılamadı")
                continue

            # Çıkış anahtar kelimesini kontrol edin
            if exit_keyword in user_question.lower():
                break

            # OpenAI'ya soruyu gönderin
            response = get_openai_response(user_question)
            print("OpenAI'nin cevabı: ", response)

            # Cevabı sesli olarak okuyun
            speak(response)

    else:
        print("Anahtar kelime algılanmadı. Programı etkinleştirmek için 'beni dinle' deyin.")
