import streamlit as st
import pandas as pd
import plotly.express  as px
import matplotlib.pyplot as plt

from db import create_table,delete_data,add_data,edit_task_data,view_all_data,get_task,view_unique_task

def main():
    st.title("ToDo App with StreamLit")

    menu=['CREATE','READ','UPDATE','DELETE','ABOUT']
    choice=st.sidebar.selectbox("Menu",menu)
    
    create_table()

    if choice=='CREATE':
        st.subheader("Add Items")

        #Layout
        col1,col2=st.columns(2)

        with col1:
            task=st.text_area("Task To Do")
        
        with col2:
            task_status=st.selectbox("Status",["ToDo","Doing","Done"])
            task_due_date=st.date_input("Due Date")

        if st.button("Add Task"):
            add_data(task,task_status,task_due_date)
            st.success("Successfully Added Data:{}".format(task))
            
    elif choice=="READ":
        with st.expander("View All"):
            result = view_all_data()
            clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
            st.dataframe(clean_df)
        
        with st.expander("Task Status"):
            task_df = clean_df['Status'].value_counts().to_frame()
            task_df = task_df.reset_index()
            st.dataframe(task_df)
            p1 = px.pie(task_df,names='Status',values='count')
            st.plotly_chart(p1,use_container_width=True)


    elif choice=='UPDATE':
        st.subheader("Edit/Update Items")
        result = view_all_data()
        clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
        with st.expander("Current Data"):
            st.dataframe(clean_df)
        
        list_of_task=[i[0] for i in view_unique_task()]
        selected_task=st.selectbox("Task to edit",list_of_task)
        
        selected_result=get_task(selected_task)
        #st.write(selected_result)

        if selected_result:
            task=selected_result[0][0]
            task_status=selected_result[0][1]
            task_due_date=selected_result[0][2]

            #Layout
            col1,col2=st.columns(2)
            with col1:
                new_task=st.text_area("Task To Do",task)
            with col2:
                new_task_status=st.selectbox(task_status,["ToDo","Doing","Done"])
                new_task_due_date=st.date_input(task_due_date)
            
            if st.button("Update Task"):
                edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
                st.success("Successfully updates::{} To ::{}".format(task,new_task))

        result2= view_all_data()
        clean_df2 = pd.DataFrame(result2,columns=["Task","Status","Date"])
        with st.expander("Updated Data"):
            st.dataframe(clean_df2)  

    elif choice=='DELETE':
        st.subheader("Delete Items")
        result= view_all_data()
        clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
        with st.expander("Current Data"):
            st.dataframe(clean_df) 

        list_of_task=[i[0] for i in view_unique_task()]
        selected_task=st.selectbox("Task to delete",list_of_task)
        st.warning("Do you want to delete {}".format(selected_task))
        if st.button("Delete Task"):
            selected_result=delete_data(selected_task) 
            st.success("task has been successfully Deleted")
        
        new_result= view_all_data()
        clean_df2 = pd.DataFrame(new_result,columns=["Task","Status","Date"])
        with st.expander("Updated Data"):
            st.dataframe(clean_df2) 
    else:
        st.subheader("About")


if __name__ =='__main__':
    main()