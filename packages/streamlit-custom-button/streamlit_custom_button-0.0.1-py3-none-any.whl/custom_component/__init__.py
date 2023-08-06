import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _custom_button = components.declare_component(
        
        "custom_button",
        
        url="http://localhost:3001",
    )
else:
    
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _custom_button = components.declare_component("custom_button", path=build_dir)

def custom_button(titles, styles, triggerButtonIcon, triggerButtonAfterIcon, key=None):

    component_value = _custom_button(titles=titles, styles=styles, triggerButtonIcon=triggerButtonIcon, triggerButtonAfterIcon=triggerButtonAfterIcon, key=key, default=0)

    return component_value

if not _RELEASE:
    import streamlit as st
    
    st.set_page_config(layout="wide")
    st.markdown('<style>' + open('D:\\component-template\\template\\my_component\\iFrame.css').read() + '</style>', unsafe_allow_html=True)
    
    st.subheader("Component with constant args")
    styles = {'selected-c':{'color':'blue'}}
    titles = [{'title':'New Template'}, 
             {'title':'Templates'}] 
    triggerButtonIcon='add'
    triggerButtonAfterIcon= 'change_history'

    num_clicks = custom_button(titles=titles, styles=styles, triggerButtonIcon=triggerButtonIcon, triggerButtonAfterIcon=triggerButtonAfterIcon)
    st.write(num_clicks)
    
