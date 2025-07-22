import streamlit as st
import psutil
from twilio.rest import Client
import pywhatkit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from urllib.parse import urljoin, urlparse
import time

# Set page config
st.set_page_config(
    page_title="Python Automation Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar with app info
with st.sidebar:
    st.title("Python Automation Dashboard")
    st.markdown("""
    **A comprehensive collection of Python automation tools:**
    - Communication tools
    - Web automation
    - Data structures
    - Image processing
    - LLM comparison
    """)
    st.markdown("---")
    st.markdown("### System Information")
    # Display RAM usage in sidebar
    virtual_memory = psutil.virtual_memory()
    st.metric("RAM Usage", f"{virtual_memory.percent}%")
    st.progress(virtual_memory.percent/100)
    st.caption(f"Used: {virtual_memory.used / (1024**3):.2f} GB / {virtual_memory.total / (1024**3):.2f} GB")

# Main app
st.title("🤖 Python Automation Dashboard")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Communication Tools", 
    "Web Automation", 
    "Data Structures", 
    "Image Processing", 
    "LLM Comparison"
])

## 1. Communication Tools Tab
with tab1:
    st.header("Communication Tools")
    
    # WhatsApp section
    with st.expander("WhatsApp Messaging"):
        whatsapp_col1, whatsapp_col2 = st.columns(2)
        
        with whatsapp_col1:
            st.subheader("Send WhatsApp Message")
            whatsapp_number = st.text_input("Recipient Number (with country code)", key="whatsapp_num")
            whatsapp_message = st.text_area("Message", key="whatsapp_msg")
            
            if st.button("Send WhatsApp Message"):
                if whatsapp_number and whatsapp_message:
                    try:
                        pywhatkit.sendwhatmsg_instantly(whatsapp_number, whatsapp_message, wait_time=15)
                        st.success("WhatsApp message sent successfully!")
                    except Exception as e:
                        st.error(f"Error sending WhatsApp message: {e}")
                else:
                    st.warning("Please enter both number and message")
        
        with whatsapp_col2:
            st.subheader("Send WhatsApp Anonymously")
            st.info("This requires a Twilio account")
            twilio_sid = st.text_input("Twilio Account SID", key="twilio_sid")
            twilio_token = st.text_input("Twilio Auth Token", type="password", key="twilio_token")
            anon_whatsapp_number = st.text_input("Recipient Number", key="anon_whatsapp_num")
            anon_whatsapp_message = st.text_area("Message", key="anon_whatsapp_msg")
            
            if st.button("Send Anonymous WhatsApp"):
                if all([twilio_sid, twilio_token, anon_whatsapp_number, anon_whatsapp_message]):
                    try:
                        client = Client(twilio_sid, twilio_token)
                        message = client.messages.create(
                            body=anon_whatsapp_message,
                            from_='whatsapp:+14155238886',
                            to=f'whatsapp:{anon_whatsapp_number}'
                        )
                        st.success(f"Anonymous message sent! SID: {message.sid}")
                    except Exception as e:
                        st.error(f"Error sending anonymous message: {e}")
                else:
                    st.warning("Please fill all fields")
    
    # Email section
    with st.expander("Email Tools"):
        email_col1, email_col2 = st.columns(2)
        
        with email_col1:
            st.subheader("Send Email")
            sender_email = st.text_input("Your Email", key="sender_email")
            sender_password = st.text_input("Your Password", type="password", key="sender_pass")
            recipient_email = st.text_input("Recipient Email", key="recipient_email")
            email_subject = st.text_input("Subject", key="email_subject")
            email_body = st.text_area("Message", key="email_body")
            
            if st.button("Send Email"):
                if all([sender_email, sender_password, recipient_email, email_subject, email_body]):
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = recipient_email
                        msg['Subject'] = email_subject
                        msg.attach(MIMEText(email_body, 'plain'))
                        
                        with smtplib.SMTP('smtp.gmail.com', 587) as server:
                            server.starttls()
                            server.login(sender_email, sender_password)
                            server.send_message(msg)
                        st.success("Email sent successfully!")
                    except Exception as e:
                        st.error(f"Error sending email: {e}")
                else:
                    st.warning("Please fill all fields")
        
        with email_col2:
            st.subheader("Send Anonymous Email")
            st.info("Note: Truly anonymous email requires special services")
            anon_sender_name = st.text_input("Sender Name", key="anon_sender")
            anon_recipient = st.text_input("Recipient Email", key="anon_recipient")
            anon_subject = st.text_input("Subject", key="anon_subject")
            anon_body = st.text_area("Message", key="anon_body")
            
            if st.button("Send Anonymous Email"):
                if all([anon_sender_name, anon_recipient, anon_subject, anon_body]):
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = anon_sender_name  # Just a name, no email
                        msg['To'] = anon_recipient
                        msg['Subject'] = anon_subject
                        msg.attach(MIMEText(anon_body, 'plain'))
                        
                        # This still requires an SMTP server - use a throwaway account
                        with smtplib.SMTP('smtp.gmail.com', 587) as server:
                            server.starttls()
                            # You'd need to configure these with a throwaway account
                            server.login('throwaway@example.com', 'password')
                            server.send_message(msg)
                        st.success("Anonymous email sent (using throwaway account)!")
                    except Exception as e:
                        st.error(f"Error sending anonymous email: {e}")
                else:
                    st.warning("Please fill all fields")
    
    # SMS & Calling section
    with st.expander("SMS & Calling"):
        sms_col1, sms_col2 = st.columns(2)
        
        with sms_col1:
            st.subheader("Send SMS")
            twilio_sid_sms = st.text_input("Twilio Account SID", key="twilio_sid_sms")
            twilio_token_sms = st.text_input("Twilio Auth Token", type="password", key="twilio_token_sms")
            from_number = st.text_input("Your Twilio Number", key="from_number")
            to_number = st.text_input("Recipient Number", key="to_number")
            sms_message = st.text_area("Message", key="sms_message")
            
            if st.button("Send SMS"):
                if all([twilio_sid_sms, twilio_token_sms, from_number, to_number, sms_message]):
                    try:
                        client = Client(twilio_sid_sms, twilio_token_sms)
                        message = client.messages.create(
                            body=sms_message,
                            from_=from_number,
                            to=to_number
                        )
                        st.success(f"SMS sent! SID: {message.sid}")
                    except Exception as e:
                        st.error(f"Error sending SMS: {e}")
                else:
                    st.warning("Please fill all fields")
        
        with sms_col2:
            st.subheader("Make Phone Call")
            st.info("Requires Twilio and a TwiML URL")
            twilio_sid_call = st.text_input("Twilio Account SID", key="twilio_sid_call")
            twilio_token_call = st.text_input("Twilio Auth Token", type="password", key="twilio_token_call")
            call_from = st.text_input("Your Twilio Number", key="call_from")
            call_to = st.text_input("Recipient Number", key="call_to")
            call_url = st.text_input("TwiML URL", key="call_url", 
                                   value="http://example.com/call_instructions.xml")
            
            if st.button("Make Call"):
                if all([twilio_sid_call, twilio_token_call, call_from, call_to, call_url]):
                    try:
                        client = Client(twilio_sid_call, twilio_token_call)
                        call = client.calls.create(
                            url=call_url,
                            to=call_to,
                            from_=call_from
                        )
                        st.success(f"Call initiated! SID: {call.sid}")
                    except Exception as e:
                        st.error(f"Error making call: {e}")
                else:
                    st.warning("Please fill all fields")

## 2. Web Automation Tab
with tab2:
    st.header("Web Automation Tools")
    
    # Google Search section
    with st.expander("Google Search"):
        search_query = st.text_input("Search Query", key="search_query")
        num_results = st.slider("Number of Results", 1, 10, 3, key="num_results")
        
        if st.button("Search Google"):
            if search_query:
                try:
                    with st.spinner("Searching Google..."):
                        search_results = list(search(search_query, num_results=num_results))
                    
                    st.subheader(f"Top {num_results} results for '{search_query}':")
                    for i, url in enumerate(search_results, 1):
                        st.write(f"{i}. [{url}]({url})")
                    
                    # Show content from first result
                    if search_results:
                        st.subheader("Content from first result:")
                        try:
                            response = requests.get(search_results[0], headers={'User-Agent': 'Mozilla/5.0'})
                            soup = BeautifulSoup(response.text, 'html.parser')
                            text_content = ' '.join(p.get_text() for p in soup.find_all('p'))
                            st.text_area("Extracted Text", value=text_content[:1000] + "...", height=200)
                        except:
                            st.warning("Could not extract content from first result")
                except Exception as e:
                    st.error(f"Error performing search: {e}")
            else:
                st.warning("Please enter a search query")
    
    # Social Media section
    with st.expander("Social Media Posting"):
        st.info("Note: Social media automation may violate terms of service. Use at your own risk.")
        
        platform = st.selectbox("Select Platform", ["Twitter/X", "Facebook", "Instagram"], key="platform")
        post_content = st.text_area("Post Content", key="post_content")
        post_image = st.file_uploader("Upload Image (optional)", type=['jpg', 'png', 'jpeg'], key="post_image")
        
        if st.button("Create Post"):
            st.warning("This is a simulation. Actual posting would require browser automation.")
            st.success(f"Simulated post to {platform} with content: {post_content[:50]}...")
    
    # Web Scraping section
    with st.expander("Website Data Download"):
        scrape_url = st.text_input("Website URL", key="scrape_url")
        max_pages = st.slider("Maximum Pages to Download", 1, 20, 5, key="max_pages")
        
        if st.button("Download Website Data"):
            if scrape_url:
                try:
                    with st.spinner(f"Downloading data from {scrape_url}..."):
                        # This is a simplified version of the web scraper
                        # In a real app, you'd want to show progress
                        visited = set()
                        to_visit = {scrape_url}
                        downloaded = 0
                        
                        if not os.path.exists("website_data"):
                            os.makedirs("website_data")
                        
                        while to_visit and downloaded < max_pages:
                            current_url = to_visit.pop()
                            
                            if current_url in visited:
                                continue
                                
                            try:
                                response = requests.get(current_url, headers={'User-Agent': 'Mozilla/5.0'})
                                visited.add(current_url)
                                downloaded += 1
                                
                                parsed_url = urlparse(current_url)
                                filename = parsed_url.path.replace('/', '_') or 'index'
                                filename = filename[:100] + '.html'
                                
                                with open(os.path.join("website_data", filename), 'w', encoding='utf-8') as f:
                                    f.write(response.text)
                                
                                soup = BeautifulSoup(response.text, 'html.parser')
                                for link in soup.find_all('a', href=True):
                                    absolute_url = urljoin(current_url, link['href'])
                                    if urlparse(absolute_url).netloc == parsed_url.netloc:
                                        if absolute_url not in visited:
                                            to_visit.add(absolute_url)
                                
                            except Exception as e:
                                st.warning(f"Error downloading {current_url}: {e}")
                    
                    st.success(f"Downloaded {downloaded} pages from {scrape_url} to 'website_data' folder")
                    st.download_button(
                        "Download as ZIP",
                        data=open("website_data", "rb").read(),
                        file_name="website_data.zip",
                        mime="application/zip"
                    )
                except Exception as e:
                    st.error(f"Error during scraping: {e}")
            else:
                st.warning("Please enter a website URL")

## 3. Data Structures Tab
with tab3:
    st.header("Python Data Structures")
    
    # Tuple vs List section
    with st.expander("Tuple vs List Comparison"):
        st.subheader("Technical Differences Between Tuples and Lists")
        
        differences = {
            "Mutability": {
                "List": "Mutable - can be changed after creation",
                "Tuple": "Immutable - cannot be changed after creation"
            },
            "Syntax": {
                "List": "Uses square brackets: [1, 2, 3]",
                "Tuple": "Uses parentheses: (1, 2, 3)"
            },
            "Performance": {
                "List": "Generally slower for iteration due to mutability overhead",
                "Tuple": "Faster iteration and access due to immutability"
            },
            "Use Cases": {
                "List": "When you need a collection that changes (add/remove items)",
                "Tuple": "When you need a fixed collection of items (coordinates, database records)"
            },
            "Memory": {
                "List": "Consumes more memory due to overhead for mutability",
                "Tuple": "More memory efficient"
            },
            "Methods": {
                "List": "Has many methods like append(), extend(), remove(), etc.",
                "Tuple": "Only has count() and index() methods"
            }
        }
        
        for category, items in differences.items():
            st.markdown(f"**{category}:**")
            st.markdown(f"- List: {items['List']}")
            st.markdown(f"- Tuple: {items['Tuple']}")
            st.write("")
        
        st.subheader("Example:")
        code = """
        my_list = [1, 2, 3]
        my_tuple = (1, 2, 3)
        
        print("Original list:", my_list)
        print("Original tuple:", my_tuple)
        
        my_list[0] = 99  # This works
        try:
            my_tuple[0] = 99  # This will raise an error
        except TypeError as e:
            print("Attempting to modify tuple results in:", str(e))
        """
        st.code(code, language='python')
    
    # RAM Info section
    with st.expander("System Information"):
        st.subheader("RAM Usage Information")
        
        virtual_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total RAM", f"{virtual_memory.total / (1024**3):.2f} GB")
            st.metric("Available RAM", f"{virtual_memory.available / (1024**3):.2f} GB")
            st.metric("Used RAM", f"{virtual_memory.used / (1024**3):.2f} GB")
        
        with col2:
            st.metric("RAM Usage Percentage", f"{virtual_memory.percent}%")
            st.metric("Total Swap", f"{swap_memory.total / (1024**3):.2f} GB")
            st.metric("Swap Used", f"{swap_memory.used / (1024**3):.2f} GB")
        
        st.progress(virtual_memory.percent/100)
        
        st.subheader("Process Memory Usage")
        process_data = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            process_data.append({
                "PID": proc.info['pid'],
                "Name": proc.info['name'],
                "Memory %": proc.info['memory_percent']
            })
        
        df_processes = pd.DataFrame(process_data).sort_values("Memory %", ascending=False).head(10)
        st.dataframe(df_processes)

## 4. Image Processing Tab
with tab4:
    st.header("Image Processing Tools")
    
    # Create Image section
    with st.expander("Create Digital Image"):
        st.subheader("Create Custom Image")
        
        width = st.slider("Width", 100, 1000, 500, key="img_width")
        height = st.slider("Height", 100, 1000, 500, key="img_height")
        bg_color = st.color_picker("Background Color", "#FFFFFF", key="bg_color")
        
        if st.button("Generate Image"):
            try:
                img = Image.new('RGB', (width, height), color=bg_color)
                draw = ImageDraw.Draw(img)
                
                # Draw some shapes
                draw.rectangle([50, 50, 150, 150], fill='blue', outline='black')
                draw.ellipse([300, 100, 400, 200], fill='red', outline='black')
                draw.polygon([(200, 300), (300, 200), (400, 300)], fill='green')
                
                # Add text
                draw.text((width//2 - 50, height - 50), "Python Generated", fill='black')
                
                st.image(img, caption="Generated Image")
                
                # Save to bytes for download
                from io import BytesIO
                buf = BytesIO()
                img.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="Download Image",
                    data=byte_im,
                    file_name="custom_image.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Error generating image: {e}")
    
    # Face Swap section
    with st.expander("Face Swapping"):
        st.subheader("Swap Faces Between Two Images")
        st.info("Note: This requires the dlib shape predictor file")
        
        col1, col2 = st.columns(2)
        
        with col1:
            image1 = st.file_uploader("Upload First Image", type=['jpg', 'png', 'jpeg'], key="face1")
            if image1:
                st.image(image1, caption="First Image", use_column_width=True)
        
        with col2:
            image2 = st.file_uploader("Upload Second Image", type=['jpg', 'png', 'jpeg'], key="face2")
            if image2:
                st.image(image2, caption="Second Image", use_column_width=True)
        
        if st.button("Swap Faces") and image1 and image2:
            st.warning("Face swapping would be implemented here with proper libraries")
            st.info("In a full implementation, this would use OpenCV and dlib to detect and swap faces")
            
            # Placeholder for face swap result
            st.image(Image.new('RGB', (500, 500), color='gray'), caption="Face Swap Result (Simulated)")

## 5. LLM Comparison Tab
with tab5:
    st.header("LLM Model Comparison")
    
    st.markdown("""
    Compare the performance of LLaMA and Alibaba's DeepSeek LLM models on various topics.
    This will evaluate their topic understanding, accuracy, and response depth.
    """)
    
    topics = [
        "climate change",
        "artificial intelligence",
        "quantum computing",
        "global economics",
        "healthcare innovations"
    ]
    
    selected_topics = st.multiselect("Select Topics to Compare", topics, default=topics[:2])
    num_prompts = st.slider("Number of Prompts per Topic", 1, 5, 2)
    
    if st.button("Run Comparison"):
        if not selected_topics:
            st.warning("Please select at least one topic")
        else:
            with st.spinner("Running comparison tests..."):
                # Simulate comparison (in reality, you'd call the actual APIs)
                results = []
                for topic in selected_topics:
                    for i in range(num_prompts):
                        prompt = f"Explain {topic} in detail with technical depth (prompt {i+1})"
                        
                        # Simulate API responses
                        llama_response = f"LLaMA response to: {prompt}. {topic} refers to..."
                        deepseek_response = f"DeepSeek response to: {prompt}. {topic} encompasses..."
                        
                        # Simulate evaluation
                        llama_score = len(llama_response.split()) // 10
                        deepseek_score = len(deepseek_response.split()) // 10
                        
                        results.append({
                            "topic": topic,
                            "prompt": prompt,
                            "llama_response": llama_response[:100] + "...",
                            "deepseek_response": deepseek_response[:100] + "...",
                            "llama_score": llama_score,
                            "deepseek_score": deepseek_score,
                            "winner": "LLaMA" if llama_score > deepseek_score else "DeepSeek"
                        })
                
                df_results = pd.DataFrame(results)
                
                st.success("Comparison completed!")
                st.subheader("Results Overview")
                
                # Summary metrics
                col1, col2, col3 = st.columns(3)
                llama_wins = len(df_results[df_results['winner'] == 'LLaMA'])
                deepseek_wins = len(df_results[df_results['winner'] == 'DeepSeek'])
                
                col1.metric("Total Tests", len(df_results))
                col2.metric("LLaMA Wins", llama_wins)
                col3.metric("DeepSeek Wins", deepseek_wins)
                
                # Detailed results
                st.subheader("Detailed Results")
                st.dataframe(df_results)
                
                # Visualization
                st.subheader("Performance Comparison")
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                
                # Score comparison by topic
                score_df = df_results.groupby('topic')[['llama_score', 'deepseek_score']].mean()
                score_df.plot(kind='bar', ax=ax1)
                ax1.set_title('Average Score by Topic')
                ax1.set_ylabel('Score')
                ax1.legend(title='Model')
                
                # Win count
                win_df = df_results['winner'].value_counts()
                win_df.plot(kind='pie', autopct='%1.1f%%', ax=ax2)
                ax2.set_title('Win Distribution')
                ax2.set_ylabel('')
                
                st.pyplot(fig)
                
                # Generate report
                report = {
                    "comparison_date": str(datetime.now()),
                    "models": ["LLaMA", "Alibaba DeepSeek"],
                    "test_topics": selected_topics,
                    "num_prompts_per_topic": num_prompts,
                    "results": results,
                    "summary": {
                        "llama_wins": llama_wins,
                        "deepseek_wins": deepseek_wins,
                        "avg_llama_score": df_results['llama_score'].mean(),
                        "avg_deepseek_score": df_results['deepseek_score'].mean()
                    }
                }
                
                # Download report
                import json
                from io import StringIO
                
                json_report = json.dumps(report, indent=2)
                st.download_button(
                    label="Download Full Report (JSON)",
                    data=StringIO(json_report).read(),
                    file_name="llm_comparison_report.json",
                    mime="application/json"
                )