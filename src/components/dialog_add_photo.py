import streamlit as st
from PIL import Image

@st.dialog("Capture or upload photos")
def add_photos_dialog():

    st.write('Add classroom photos to scan for attendance')

    # Use a staging list, separate from the real list
    if 'staged_images' not in st.session_state:
        st.session_state.staged_images = []

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Camera', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload photos', type=type_upload, width='stretch'):
            st.session_state.photo_tab = 'upload'

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo:
            img = Image.open(cam_photo)
            # Only stage if not already added (avoid duplicates on rerun)
            if img not in st.session_state.staged_images:
                st.session_state.staged_images.append(img)
            st.toast(f'Photo staged ({len(st.session_state.staged_images)} total)')

    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader(
            'choose image files',
            type=['jpg', 'png', 'jpeg'],
            accept_multiple_files=True,
            key='dialog_upload'
        )
        if uploaded_files:
            st.session_state.staged_images = [Image.open(f) for f in uploaded_files]
            st.toast(f'{len(uploaded_files)} photo(s) ready — click Done to add')

    if st.session_state.staged_images:
        st.caption(f'✅ {len(st.session_state.staged_images)} photo(s) ready to add')

    st.divider()

    if st.button('Done', type='primary', width='stretch'):
        if 'attendance_images' not in st.session_state:
            st.session_state.attendance_images = []

        st.session_state.attendance_images.extend(st.session_state.staged_images)
        st.session_state.staged_images = []  
        st.rerun()