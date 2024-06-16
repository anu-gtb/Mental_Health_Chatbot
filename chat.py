import streamlit as st 
import speech_recognition as sr
from transformers import GPT2LMHeadModel,GPT2Tokenizer

model_path='Mental_Health_Chatbot/model'

st.set_page_config('Mental Health Chatbot')

st.title('Mental Health Center')

if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]
    
prompt = st.text_input('type your query')

update=st.button('Send/Update')

with st.chat_message(name='assistant'):
    st.write('Welcome!:slightly_smiling_face: How can I help you today?')

def load_model(model_path):
    model=GPT2LMHeadModel.from_pretrained(model_path)
    return model

def load_tokenizer(tokenizer_path):
    tokenizer=GPT2Tokenizer.from_pretrained(tokenizer_path)
    return tokenizer

def remove_numbers(text):
 return ''.join(char for char in text if not char.isdigit())

def replace(text):
    return text.replace('\n','')

def generate_text(model_path,sequence):
    model=load_model(model_path)
    tokenizer=load_tokenizer(model_path)
    IDs=tokenizer.encode(sequence,return_tensors='pt')
    outputs=model.generate(IDs,max_length=100,pad_token_id=model.config.eos_token_id,top_k=50,top_p=0.97)
    return tokenizer.decode(outputs[0],skip_special_tokens=True)

if update:
    if prompt!='':
        st.write(
            f'<div style="display:flex; align-items:center; flex-direction:row-reverse;">'
            f'<div style="margin-right: 10px;">'
            f'</div>'
            f'<div style="background-color:#d3d3d3; padding:10px; border_radius:10px;">'
            f'{prompt}'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        st.session_state['chat_history'].append(prompt)
        if prompt=='hey' or prompt=='hi' or prompt=='hello' or prompt=='i need help' or prompt=='is anybody there':
            st.write(
            f'<div style="display:flex; align-items:center;">'
            f'<div style="margin-right: 10px;">'
            f'</div>'
            f'<div style="background-color:#d3d3d3; padding:10px; border_radius:10px;">'
            f'Hello! Please Tell me your query.'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        if prompt=='thank you' or prompt=='thanks' or prompt=='ok' or prompt=='okay' or prompt=='thank you so much' or prompt=='thanks a lot'  or prompt=='bye' or prompt=='got it':
          st.write(
            f'<div style="display:flex; align-items:center;">'
            f'<div style="margin-right: 10px;">'
            f'</div>'
            f'<div style="background-color:#d3d3d3; padding:10px; border_radius:10px;">'
            f'Thanks for visiting. Have a nice day!&#128077'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        if prompt!='hi' and prompt!='hey' and prompt!='hello' and prompt!='is anybody there?' and prompt!='i need help' and prompt!='thanks' and prompt!='thanks a lot' and prompt!='thank you' and prompt!='thank you so much' and prompt!='got it' and prompt!='bye' and prompt!='ok' and prompt!='okay':
            result=generate_text(model_path,prompt)
            st.write(
            f'<div style="display:flex; align-items:center;">'
            f'<div style="margin-right: 10px;">'
            f'</div>'
            f'<div style="background-color:#d3d3d3; padding:10px; border_radius:10px;">'
            f'{result}'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
           )       
        
subheader_text = "*Press END button after query is solved"
style = f"<p style='font-size:13px;font-family:serif'> {subheader_text} </p>"
st.markdown(style, unsafe_allow_html=True)

end=st.button('END')

if end:
    st.write('The conversation has ended')
        
speak = st.button("Speak Query:microphone:")

def record_audio():
   rec=sr.Recognizer()
   with sr.Microphone() as mic:
        st.write('Listening...')
        audio=rec.listen(mic)
   try:
        text=rec.recognize_google(audio)
        return text
   except sr.UnknownValueError:
        st.error('Speak again')
   except sr.RequestError as re:
        st.error(re)

if speak:
    text=record_audio()
    st.text_input(label='Your text',value=text)
    if text=='hey' or text=='hi' or text=='hello' or text=='i need help' or text=='is anybody there':
        st.write('Ans : Hello! Please Tell me your query.')
    if text=='thank you' or text=='thanks' or text=='ok' or text=='okay' or text=='thank you so much' or text=='thanks a lot'  or text=='bye' or text=='got it':
        st.write('Ans : Thanks for visiting. Have a nice day!&#128077')
    if text!='hi' and text!='hey' and text!='hello' and text!='is anybody there?' and text!='i need help' and text!='thanks' and text!='thanks a lot' and text!='thank you' and text!='thank you so much' and text!='got it' and text!='bye' and text!='ok' and text!='okay':
        res=generate_text(model_path,text)
        st.write('Ans :',res)
    
st.subheader('OR')

subheader_text = "You can also upload a file containing your query below :"
style = f"<p style='font-size:20px;font-family:serif'> {subheader_text} </p>"
st.markdown(style, unsafe_allow_html=True)

file=st.file_uploader('Drop text document only')
generate=st.button('GO')

if generate:
  if file is not None:
    if file.type=='text/plain':
        content=file.read().decode('utf-8')
        if content=='hey' or content=='hi' or content=='hello' or content=='i need help' or content=='is anybody there':
            st.write('Hello! Please Tell me your query.')
        if content=='thank you' or content=='thanks' or content=='ok' or content=='okay' or content=='thank you so much' or content=='thanks a lot'  or content=='bye' or content=='got it':
            st.write('Thanks for visiting. Have a nice day!&#128077')
        if content!='hi' and content!='hey' and content!='hello' and content!='is anybody there?' and content!='i need help' and content!='thanks' and content!='thanks a lot' and content!='thank you' and content!='thank you so much' and content!='got it' and content!='bye' and content!='ok' and content!='okay':
            res=generate_text(model_path,text)
            st.write(res)
    else:
        st.error('Unsupported file format!')  
    
        
    



    
    
    
    
    
    
    
    
    
    
    
