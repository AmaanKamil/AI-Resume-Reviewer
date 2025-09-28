# import streamlit as st
# import requests
# import tempfile
# import os

# # Configuration - Replace with your actual values
# LANGFLOW_URL = "http://localhost:7860"
# FLOW_ID = "87515769-614a-402f-930f-6455a49bccba" 
# API_KEY = "sk-Db8YhDdknWt0AOEZWzOD02UMJKNyMWehx1WmmfwhJpU"
# FILE_COMPONENT_ID = "File-nHk6A"

# def upload_file_and_run_analysis(file, flow_id, job_description=""):
#     """Combined approach - upload file and run analysis in one go"""
    
#     try:
#         # Step 1: Upload file to LangFlow's file system
#         upload_url = f"{LANGFLOW_URL}/api/v1/files/upload/{flow_id}"
        
#         files = {"file": (file.name, file.getvalue(), file.type)}
#         headers = {"x-api-key": API_KEY}
        
#         st.write(f"🔄 Uploading file to: {upload_url}")
#         upload_response = requests.post(upload_url, files=files, headers=headers)
        
#         st.write(f"📊 Upload Status: {upload_response.status_code}")
        
#         if upload_response.status_code not in [200, 201]:
#             st.error(f"Upload failed: {upload_response.text}")
#             return None
            
#         # Get the uploaded file path
#         upload_data = upload_response.json()
#         st.success("✅ File uploaded successfully!")
#         st.write(f"📁 File path: {upload_data}")
        
#         # Step 2: Run analysis using tweaks (the working method from GitHub)
#         run_url = f"{LANGFLOW_URL}/api/v1/run/{flow_id}"
        
#         # Build the payload with tweaks approach
#         message = "Please analyze the uploaded resume file."
#         if job_description.strip():
#             message += f" Here's the job description: {job_description}"
        
#         payload = {
#             "input_value": message,
#             "output_type": "chat", 
#             "input_type": "chat",
#             "tweaks": {
#                 # You need to replace "File-XXXX" with your actual File component ID
#                 # You can find this ID in your LangFlow flow
#                 "File-COMPONENT-ID": {  # Replace with actual File component ID
#                     "path": upload_data.get("path", "")  # Use the uploaded file path
#                 }
#             }
#         }
        
#         headers = {
#             "Content-Type": "application/json",
#             "x-api-key": API_KEY
#         }
        
#         st.write("🤖 Running analysis...")
#         analysis_response = requests.post(run_url, json=payload, headers=headers)
        
#         st.write(f"📊 Analysis Status: {analysis_response.status_code}")
        
#         if analysis_response.status_code == 200:
#             return analysis_response.json()
#         else:
#             st.error(f"Analysis failed: {analysis_response.text}")
#             return None
            
#     except Exception as e:
#         st.error(f"❌ Error: {str(e)}")
#         return None


# # def analyze_resume(message):
# #     """Run the LangFlow analysis"""
# #     url = f"{LANGFLOW_URL}/api/v1/run/{FLOW_ID}"
    
# #     payload = {
# #         "input_value": message,
# #         "output_type": "chat",
# #         "input_type": "chat"
# #     }
    
# #     headers = {
# #         "Content-Type": "application/json",
# #         "x-api-key": API_KEY
# #     }
    
# #     response = requests.post(url, json=payload, headers=headers)
# #     return response.json()

# # Streamlit UI
# st.set_page_config(
#     page_title="AI Resume Reviewer",
#     page_icon="🤖",
#     layout="wide"
# )

# st.title("🤖 AI Resume Reviewer")
# st.write("Upload your resume and get instant AI-powered feedback!")

# # File upload
# uploaded_file = st.file_uploader(
#     "📄 Choose your resume file", 
#     type=['pdf', 'doc', 'docx'],
#     help="Upload your resume in PDF, DOC, or DOCX format"
# )

# # Job description input
# job_description = st.text_area(
#     "📋 Job Description (Optional)",
#     placeholder="Paste the job description here for targeted feedback...",
#     height=100
# )

# # Analyze button
# if st.button("🚀 Analyze Resume", type="primary"):
#     if uploaded_file is not None:
#         result = upload_and_analyze_resume(uploaded_file, job_description)
        
#         if result:
#             st.success("🎉 Analysis Complete!")
#             # Display results as before

# # if st.button("🚀 Analyze Resume", type="primary"):
# #     if uploaded_file is not None:
# #         with st.spinner("📊 Analyzing your resume..."):
# #             try:
# #                 # Upload file
# #                 upload_response = upload_file_to_langflow(uploaded_file, FLOW_ID)
                
# #                 if upload_response.status_code == 200:
# #                     # Prepare message
# #                     message = f"Please analyze the uploaded resume."
# #                     if job_description:
# #                         message += f" Job Description: {job_description}"
                    
# #                     # Run analysis
# #                     result = analyze_resume(message)
                    
# #                     # Display results
# #                     st.success("✅ Analysis Complete!")
                    
# #                     with st.container():
# #                         st.subheader("📋 Analysis Results:")
# #                         # Extract the response text from the result
# #                         if 'outputs' in result:
# #                             analysis_text = result['outputs'][0]['outputs'][0]['results']['message']['data']['text']
# #                             st.write(analysis_text)
# #                         else:
# #                             st.write(result)
                            
# #                 else:
# #                     st.error("❌ File upload failed. Please try again.")
                    
# #             except Exception as e:
# #                 st.error(f"❌ Error: {str(e)}")
# #     else:
# #         st.warning("⚠️ Please upload a resume file first!")

# # Instructions
# with st.expander("ℹ️ How to use"):
#     st.write("""
#     1. **Upload your resume** in PDF, DOC, or DOCX format
#     2. **Optionally paste a job description** for targeted feedback
#     3. **Click 'Analyze Resume'** to get AI-powered feedback
#     4. **Review the analysis** including ATS score, strengths, and recommendations
#     """)


import streamlit as st
import requests
from PyPDF2 import PdfReader
import io

# Configuration - Replace with your actual values
LANGFLOW_URL = "http://localhost:7860"  # Replace with your LangFlow URL
FLOW_ID = "87515769-614a-402f-930f-6455a49bccba"           # Replace with your Flow ID
API_KEY = "sk-Db8YhDdknWt0AOEZWzOD02UMJKNyMWehx1WmmfwhJpU"           # Replace with your API Key

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file using PyPDF2"""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def upload_file_to_langflow(file_path, flow_id):
    """Upload file to LangFlow using the working endpoint from GitHub"""
    url = f"{LANGFLOW_URL}/api/v1/upload/{flow_id}"
    
    headers = {"x-api-key": API_KEY}
    
    try:
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = requests.post(url, files=files, headers=headers)
            
        if response.status_code in [200, 201]:
            return response.json()
        else:
            st.error(f"Upload failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Upload error: {str(e)}")
        return None

def analyze_with_tweaks(message, file_component_id=None, file_path=None):
    """Run analysis using the tweaks method from GitHub solution"""
    url = f"{LANGFLOW_URL}/api/v1/run/{FLOW_ID}"
    
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat"
    }
    
    # Add tweaks if file info is provided
    if file_component_id and file_path:
        payload["tweaks"] = {
            file_component_id: {"path": file_path}
        }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Analysis failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def analyze_with_extracted_text(resume_text, job_description=""):
    """Analyze resume using extracted text (fallback method)"""
    url = f"{LANGFLOW_URL}/api/v1/run/{FLOW_ID}"
    
    message = f"Please analyze this resume text and provide detailed feedback:\n\n{resume_text}"
    if job_description.strip():
        message += f"\n\nJob Description for targeted analysis:\n{job_description}"
    
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat"
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Analysis failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Streamlit UI
st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Resume Reviewer")
st.write("Upload your resume and get instant AI-powered feedback!")

# Sidebar for configuration
with st.sidebar:
    st.header("🔧 Configuration")
    st.write(f"**LangFlow URL:** {LANGFLOW_URL}")
    st.write(f"**Flow ID:** {FLOW_ID[:8]}...")
    
    # File Component ID input (needed for tweaks method)
    file_component_id = st.text_input(
        "File Component ID (optional):", 
        placeholder="File-abc123...",
        help="Find this in your LangFlow flow by clicking on the File component"
    )
    
    if st.button("Test Connection"):
        try:
            test_url = f"{LANGFLOW_URL}/api/v1/flows/{FLOW_ID}"
            response = requests.get(test_url, headers={"x-api-key": API_KEY})
            if response.status_code == 200:
                st.success("✅ Connection successful!")
            else:
                st.error(f"❌ Connection failed: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Connection error: {str(e)}")

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    # File upload
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader(
        "Choose your resume file", 
        type=['pdf'],
        help="Upload your resume in PDF format"
    )
    
    # Job description
    st.subheader("📋 Job Description (Optional)")
    job_description = st.text_area(
        "Paste job description here:",
        placeholder="Paste the job description here for targeted feedback...",
        height=150
    )

with col2:
    st.markdown("""
    ### 📝 How to use:
    
    1. **Upload your PDF resume**
    2. **Add job description** (optional)
    3. **Click 'Analyze Resume'**
    4. **Get detailed feedback**
    
    ### 📊 Analysis includes:
    - ATS compatibility score
    - Key strengths
    - Areas for improvement
    - Specific recommendations
    - Job match analysis
    
    ### 🔧 For advanced users:
    Add your File Component ID in the sidebar for direct file upload to LangFlow.
    """)

# Analyze button
if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
    if uploaded_file is not None:
        with st.spinner("📊 Processing your resume..."):
            
            # Method 1: Try direct file upload if component ID is provided
            if file_component_id.strip():
                with st.status("Uploading file to LangFlow...", expanded=True) as status:
                    # Save uploaded file temporarily
                    temp_file_path = f"temp_{uploaded_file.name}"
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Upload to LangFlow
                    upload_result = upload_file_to_langflow(temp_file_path, FLOW_ID)
                    
                    if upload_result:
                        status.update(label="✅ File uploaded successfully!", state="complete")
                        
                        # Run analysis with tweaks
                        message = "Please analyze the uploaded resume file."
                        if job_description.strip():
                            message += f" Job description: {job_description}"
                        
                        result = analyze_with_tweaks(message, file_component_id, upload_result.get("path"))
                        
                        # Clean up temp file
                        import os
                        try:
                            os.remove(temp_file_path)
                        except:
                            pass
                            
                    else:
                        status.update(label="❌ File upload failed, using text extraction", state="error")
                        result = None
            
            # Method 2: Fallback - Extract text and send as message
            if not file_component_id.strip() or 'result' not in locals() or result is None:
                with st.status("Extracting text from PDF...", expanded=True) as status:
                    resume_text = extract_text_from_pdf(uploaded_file)
                    
                    if resume_text:
                        status.update(label="✅ Text extracted successfully!", state="complete")
                        
                        with st.status("Analyzing resume...", expanded=True) as analysis_status:
                            result = analyze_with_extracted_text(resume_text, job_description)
                            
                            if result:
                                analysis_status.update(label="✅ Analysis complete!", state="complete")
                            else:
                                analysis_status.update(label="❌ Analysis failed!", state="error")
                    else:
                        status.update(label="❌ Text extraction failed!", state="error")
                        result = None
            
            # Display results
            if result:
                st.success("🎉 Analysis Complete!")
                
                with st.container():
                    st.subheader("📋 Resume Analysis Results:")
                    
                    try:
                        # Parse the response
                        if 'outputs' in result and result['outputs']:
                            output = result['outputs'][0]
                            if 'outputs' in output and output['outputs']:
                                analysis_result = output['outputs'][0]
                                if 'results' in analysis_result:
                                    message_data = analysis_result['results']['message']['data']
                                    analysis_text = message_data['text']
                                    st.markdown(analysis_text)
                                else:
                                    st.json(result)
                            else:
                                st.json(result)
                        else:
                            st.json(result)
                            
                    except (KeyError, IndexError, TypeError) as e:
                        st.warning("Could not parse response format. Raw output:")
                        st.json(result)
            else:
                st.error("❌ Analysis failed. Please check your configuration and try again.")
                
    else:
        st.warning("⚠️ Please upload a PDF file first!")

# Footer
st.markdown("---")
st.markdown("**Built with LangFlow + Streamlit** | Upload your resume PDF to get started!")

# Instructions for finding File Component ID
with st.expander("🔍 How to find your File Component ID"):
    st.markdown("""
    1. **Go to your LangFlow flow editor**
    2. **Click on your File component**  
    3. **Look for the component ID** (usually shows as "File-" followed by letters/numbers)
    4. **Copy and paste it** in the sidebar configuration
    5. **This enables direct file upload to LangFlow**
    
    **Without Component ID**: The app will extract text from your PDF and send it as a message (still works great!)
    """)
