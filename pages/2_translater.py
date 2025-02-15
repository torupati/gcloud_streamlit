import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st


st.set_page_config(page_title="Application", page_icon=":shark:")
st.title("Translation Application")
print("Redrow")
source_language = ["English", "Japanese", "Korea", "Chinese"]

def translate(source: str, target: str, input: str) -> str:
    model = ChatOpenAI(model="gpt-4o-2024-05-13")
    parser = StrOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Translate the following {source_language} to {target_language}"),
        ("user", "{user_input}"),
    ])
    chain = prompt | model | parser
    return chain.invoke({
        "source_language": source,
        "target_language": target,
        "user_input": input
    })

def swap_selectbox_value():
    st.session_state.target, st.session_state.source = st.session_state.source, st.session_state.target
    if "output" in st.session_state and st.session_state.output != "":
        st.session_state.input = st.session_state.output
    

row1_left, row1_center, row1_right = st.columns((4, 2, 4))
row2_left, row2_right = st.columns(2)

with row1_left:
    print(f"{'source' in st.session_state=}") # => None
    source = st.selectbox(
        'Source Language', source_language, label_visibility="collapsed",
        key="source"
    )
    print(f"{'source' in st.session_state=}") # => True
    print(f"{st.session_state.source=}")

with row1_right:
    target_languages = [l for l in source_language if l != source]
    index = 0
    #if "target" in st.session_state and st.session_state.tartet != source:
    #    index = target_languages.index(st.session_state.target)
    target = st.selectbox(
        "target language", target_languages, label_visibility='collapsed',
        key = "target", index=index
    )
    #st.session_state.source = "Japanese"

with row1_center:
    if st.button('<->', type='secondary', use_container_width=True,
                 on_click=swap_selectbox_value):
        pass

with row2_left:
    input = st.text_area(
        'Input Text', label_visibility='collapsed', height=200, placeholder="Input text you want to translate",
        key = "input"
    )

with row2_right:
    if input != "":
        with st.spinner('Translating...'):
            #time.sleep(3)
            #st.write("[Dummy message]")
            output = translate(source, target, input)
            st.session_state.output = output
            print(f"{output=}")
            st.write(output)

