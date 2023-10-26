from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2


import uuid

import streamlit as st
from base_campaign_workflow import base_campaign_post_generator
from base_tts import base_tts_call, convert_base64_to_bytes, limit_string_to_500_characters
from moderation_model import moderate_text
from translation_workflow import spanish_translate, arabic_translate, chinese_translate
from sigma_workflow import sigma_output
import io
from PIL import Image
import base64
from qr_generator import get_qr_image

import modal

CLARIFAI_PAT = st.secrets.CLARIFAI_PAT
MODERATION_THRESHOLD = st.secrets.MODERATION_THRESHOLD

st.set_page_config(page_title="Campaign Alchemist", page_icon="", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

st.title(body="Campaign Alchemist 🤖")


def initialize_session_state():
    if "base_english_post" not in st.session_state:
        st.session_state.base_english_post = None

    if "base_spanish_post" not in st.session_state:
        st.session_state.base_spanish_post = None

    if "base_chinese_post" not in st.session_state:
        st.session_state.base_chinese_post = None

    if "base_arabic_post" not in st.session_state:
        st.session_state.base_arabic_post = None

    if "bulk_english_post" not in st.session_state.keys():
        st.session_state.bulk_english_post = None

    if "bulk_spanish_post" not in st.session_state.keys():
        st.session_state.bulk_spanish_post = None

    if "bulk_chinese_post" not in st.session_state.keys():
        st.session_state.bulk_chinese_post = None

    if "bulk_arabic_post" not in st.session_state.keys():
        st.session_state.bulk_arabic_post = None

    if "base_english_audio" not in st.session_state:
        st.session_state.base_english_audio = None

    if "base_spanish_audio" not in st.session_state:
        st.session_state.base_spanish_audio = None

    if "base_chinese_audio" not in st.session_state:
        st.session_state.base_chinese_audio = None

    if "base_arabic_audio" not in st.session_state:
        st.session_state.base_arabic_audio = None

    if "bulk_english_audio" not in st.session_state:
        st.session_state.bulk_english_audio = None

    if "bulk_spanish_audio" not in st.session_state:
        st.session_state.bulk_spanish_audio = None

    if "bulk_chinese_audio" not in st.session_state:
        st.session_state.bulk_chinese_audio = None

    if "bulk_arabic_audio" not in st.session_state:
        st.session_state.bulk_arabic_audio = None

    if "bulk_image" not in st.session_state:
        st.session_state.bulk_image = None

    if "qr_code" not in st.session_state:
        st.session_state.qr_code = None


initialize_session_state()

tab1, tab2, tab3 = st.tabs(["AI Post Generator(Short with Audio)", "AI Post Generator(Long)",
                            "AI Qr Code Generator"])

with tab1:
    st.header("Generate Posts for a product/feature/firm for social media")
    user_product_input = st.text_input("Enter the description of the product/feature/ firm you want to promote",
                               """Copilot is here! Mindtickle has released a suite of generative AI features across its revenue productivity platform to help everyone in the revenue organization.

Generating revenue doesn’t fall on one department, it’s a critical responsibility across go-to-market teams including sellers, enablement, customer success, operations, and management. Yet 72% of salespeople expect their team to miss annual quota in 2023 according to Salesforce.

Recent generative AI technologies have the ability to make these teams more productive so they can focus on their high-value revenue-generating activities.

That’s where Copilot comes in.

Copilot helps revenue teams:

    Discover data-driven insights faster
    Create personalized experiences quickly
    Execute revenue-generating interactions exceptionally
    Uphold security and ethical standards with a secure generative AI platform

This not only saves time for enablement professionals but also ensures that sales teams have access to up-to-date, engaging, and tailored content that resonates with their target audience.
Discover data-driven insights faster

Copilot gets you the answers you need to make data-based decisions, without reviewing lengthy calls or navigating dashboards and reporting pages.
AI call navigator

Get quick insights into every call fast

Copilot can analyze any call in seconds and answer top-of-mind questions without having to sift through a transcript. Sellers can get a quick call summary, craft detailed follow-ups, and receive self-coaching tips on how to improve future customer and prospect interactions. Managers can prioritize reps to coach by call scores and quickly review underperforming calls to foster detailed coaching sessions.
""")

    if st.button("Generate Campaign Post in English"):
        with st.spinner(text="Using ClarifAI workflow to generate English Post and English Audio"):
            try:
                reason, intervene = moderate_text(text=user_product_input, clarif_ai_pat=CLARIFAI_PAT,
                                                  moderation_threshold=MODERATION_THRESHOLD)
            except Exception as e:
                print(str(e))
                reason = ''
                intervene = False
            if not intervene:
                st.session_state.base_english_post = base_campaign_post_generator(product_description=user_product_input,
                                                                                  clarif_ai_pat=CLARIFAI_PAT)
                if st.session_state.base_english_post is not None and st.session_state.base_english_post != "There has been an exception":

                    base_english_text = st.session_state.base_english_post
                    try:
                        truncated_base_english_text = limit_string_to_500_characters(input_text=base_english_text)
                    except Exception as e:
                        truncated_base_english_text = base_english_text[0:500]

                    st.session_state.base_english_audio = base_tts_call(input_text=truncated_base_english_text,
                                                                        clarif_ai_pat=CLARIFAI_PAT)
            else:
                response = f"This description cannot be processed as it has been detected to be {reason}"
                st.write(response)
        st.success('Done!')

    if st.session_state.base_english_post is not None and st.session_state.base_english_post != "There has been an exception":
        with st.expander("See English Post"):
            st.markdown(st.session_state.base_english_post)

    if st.session_state.base_english_audio is not None and st.session_state.base_english_audio != "There has been an exception":
        st.audio(data=st.session_state.base_english_audio)

    if st.session_state.base_english_post is not None and st.session_state.base_english_post != "There has been an exception":
        if st.button("Generate Campaign Post in Spanish"):
            with st.spinner(text="Using ClarifAI workflow to generate Spanish Post and Spanish Audio"):
                try:
                    base_english_text = st.session_state.base_english_post
                    try:
                        truncated_base_english_text = limit_string_to_500_characters(input_text=base_english_text)
                    except Exception as e:
                        truncated_base_english_text = base_english_text[0:500]

                    st.session_state.base_spanish_post, st.session_state.base_spanish_audio = spanish_translate(input_text=truncated_base_english_text, clarif_ai_pat=CLARIFAI_PAT)
                except TypeError as e:
                    st.write("Unable to generate")
                except ValueError as e:
                    st.write("Unable to generate")

            st.success('Done!')

        if st.button("Generate Campaign Post in Chinese"):
            with st.spinner(text="Using ClarifAI workflow to generate Chinese Post and Chinese Audio"):
                base_english_text = st.session_state.base_english_post
                try:
                    try:
                        truncated_base_english_text = limit_string_to_500_characters(input_text=base_english_text)
                    except Exception as e:
                        truncated_base_english_text = base_english_text[:500]
                    st.session_state.base_chinese_post, st.session_state.base_chinese_audio = chinese_translate(input_text=truncated_base_english_text,
                                                                           clarif_ai_pat=CLARIFAI_PAT)
                except TypeError as e:
                    st.write("Unable to generate")
                except ValueError as e:
                    st.write("Unable to generate")

            st.success('Done!')

        if st.button("Generate Campaign Post in Arabic"):
            with st.spinner(text="Using ClarifAI workflow to generate arabic Post and arabic Audio"):
                base_english_text = st.session_state.base_english_post
                try:
                    try:
                        truncated_base_english_text = limit_string_to_500_characters(input_text=base_english_text)
                    except Exception as e:
                        truncated_base_english_text = base_english_text[0:500]
                    st.session_state.base_arabic_post, st.session_state.base_arabic_audio = arabic_translate(input_text=truncated_base_english_text,
                                                                           clarif_ai_pat=CLARIFAI_PAT)
                except TypeError as e:
                    st.write("Unable to generate")
                except ValueError as e:
                    st.write("Unable to generate")

            st.success('Done!')

    if st.session_state.base_spanish_post is not None and st.session_state.base_spanish_post != "Default":
        with st.expander("See Spanish Post"):
            st.markdown(st.session_state.base_spanish_post)

    if st.session_state.base_spanish_audio is not None and st.session_state.base_spanish_audio != "Default":
        st.audio(data=st.session_state.base_spanish_audio)

    if st.session_state.base_chinese_post is not None and st.session_state.base_chinese_post != "Default":
        with st.expander("See chinese Post"):
            st.markdown(st.session_state.base_chinese_post)

    if st.session_state.base_chinese_audio is not None and st.session_state.base_chinese_audio != "Default":
        st.audio(data=st.session_state.base_chinese_audio)

    if st.session_state.base_arabic_post is not None and st.session_state.base_arabic_post != "Default":
        with st.expander("See arabic Post"):
            st.markdown(st.session_state.base_arabic_post)

    if st.session_state.base_arabic_audio is not None and st.session_state.base_arabic_audio != "Default":
        st.audio(data=st.session_state.base_arabic_audio)


with tab2:
    st.header("Generate Posts for a product/feature/firm for social media directly in multiple languages")
    st.info("Do note this a relatively slower option as it bulk calls all AI models to generate output in all supported languages", icon="ℹ️")
    user_product_input_bulk = st.text_input("Enter the description of the product/feature/ firm you want to promote",
                                       """Copilot is here! Mindtickle has released a suite of generative AI features across its revenue productivity platform to help everyone in the revenue organization.
    
        Generating revenue doesn’t fall on one department, it’s a critical responsibility across go-to-market teams including sellers, enablement, customer success, operations, and management. Yet 72% of salespeople expect their team to miss annual quota in 2023 according to Salesforce.
    
        Recent generative AI technologies have the ability to make these teams more productive so they can focus on their high-value revenue-generating activities.
    
        That’s where Copilot comes in.
    
        Copilot helps revenue teams:
    
            Discover data-driven insights faster
            Create personalized experiences quickly
            Execute revenue-generating interactions exceptionally
            Uphold security and ethical standards with a secure generative AI platform
    
        This not only saves time for enablement professionals but also ensures that sales teams have access to up-to-date, engaging, and tailored content that resonates with their target audience.
        Discover data-driven insights faster
    
        Copilot gets you the answers you need to make data-based decisions, without reviewing lengthy calls or navigating dashboards and reporting pages.
        AI call navigator
    
        Get quick insights into every call fast
    
        Copilot can analyze any call in seconds and answer top-of-mind questions without having to sift through a transcript. Sellers can get a quick call summary, craft detailed follow-ups, and receive self-coaching tips on how to improve future customer and prospect interactions. Managers can prioritize reps to coach by call scores and quickly review underperforming calls to foster detailed coaching sessions.""")

    if st.button("Generate Campaign Posts(Multilingual)"):
        with st.spinner(text="Using ClarifAI workflow to generate Multilingual Posts"):
            try:
                reason, intervene = moderate_text(text=user_product_input_bulk, clarif_ai_pat=CLARIFAI_PAT,
                                                  moderation_threshold=MODERATION_THRESHOLD)
            except Exception as e:
                print(str(e))
                reason = ''
                intervene = False
            if not intervene:
                try:
                    st.session_state.bulk_arabic_post,\
                    st.session_state.bulk_chinese_post, st.session_state.bulk_spanish_post, \
                    st.session_state.bulk_english_post = sigma_output(input_text=user_product_input_bulk,
                                                                      clarif_ai_pat=CLARIFAI_PAT)
                except Exception as e:
                    print(f"{str(e)}")
                    st.write("Unable to Generate")
            else:
                response = f"This description cannot be processed as it has been detected to be {reason}"
                st.write(response)

        st.success('Done!')

    if st.session_state.bulk_english_post is not None and st.session_state.bulk_english_post != "Default":
        with st.expander("See English Post"):
            st.markdown(st.session_state.bulk_english_post)

    if st.session_state.bulk_spanish_post is not None and st.session_state.bulk_spanish_post != "Default":
        with st.expander("See Spanish Post"):
            st.markdown(st.session_state.bulk_spanish_post)

    if st.session_state.bulk_chinese_post is not None and st.session_state.bulk_chinese_post != "Default":
        with st.expander("See Chinese Post"):
            st.markdown(st.session_state.bulk_chinese_post)

    if st.session_state.bulk_arabic_post is not None and st.session_state.bulk_arabic_post != "Default":
        with st.expander("See Arabic Post"):
            st.markdown(st.session_state.bulk_arabic_post)


with tab3:
    st.header("Generate Cool and Quirky QR codes embedded within Images")
    input_content = st.text_input("Enter content you want to be embedded in the QR code", "https://aclanthology.org/2023.semeval-1.266/")
    prompt = st.text_input("Write text description of the image in which you want the Qr code to be embedded", "Natural ice cream flavours")

    if st.button("Submit"):
        with st.spinner(text="Generating beautiful and aesthetic qr code embedded images"):
            qr_image = get_qr_image(qr_code_content=input_content,prompt=prompt)
            st.session_state.qr_code = qr_image

    if st.session_state.qr_code is not None and st.session_state.qr_code != "Default":
        st.image(st.session_state.qr_code)



















