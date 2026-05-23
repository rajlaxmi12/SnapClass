import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

import time


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    if st.button('Enroll now', type='primary', width='stretch'):
        if not join_code:
            st.warning('Please enter a subject code')
            st.stop()

        student_id = None
        if 'student_data' in st.session_state and st.session_state['student_data']:
            student_id = st.session_state.student_data.get('student_id')

        if not student_id:
            st.error('Student session not found. Please login again.')
            st.stop()

        res = (
            supabase.table('subjects')
            .select('subject_id, name, subject_code')
            .eq('subject_code', join_code)
            .execute()
        )
        if getattr(res, 'data', None):
            subject = res.data[0]
        else:
            st.error(f"Subject not found for code '{join_code}'.")
            if getattr(res, 'error', None):
                st.caption(str(res.error))
            st.stop()

        check = (
            supabase.table('subject_students')
            .select('*')
            .eq('subject_id', subject['subject_id'])
            .eq('student_id', student_id)
            .execute()
        )

        if getattr(check, 'error', None):
            st.error('Enrollment check query failed.')
            st.caption(str(check.error))
            st.stop()

        if getattr(check, 'data', None):
            st.warning('You are already enrolled in this program')
            st.stop()

        try:
            insert_res = enroll_student_to_subject(student_id, subject['subject_id'])
        except Exception as e:
            st.error('Enrollment insert crashed.')
            st.caption(str(e))
            st.stop()

        st.success('Succesfully enrolled!')
        time.sleep(1)
        st.rerun()
