import streamlit as st
import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('crud_app.db')
    except Error as e:
        st.write(e)
    return conn

def create_table(conn):
    try:
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        description text
                                    ); """
        conn.execute(sql_create_projects_table)
    except Error as e:
        st.write(e)

def add_project(conn, project):
    sql = ''' INSERT INTO projects(name,description)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()

def get_projects(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects")
    rows = cur.fetchall()
    return rows

def update_project(conn, project):
    sql = ''' UPDATE projects
              SET name = ? ,
                  description = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()

def delete_project(conn, id):
    sql = 'DELETE FROM projects WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def main():
    st.title("Produk Nozy Juice")
    
    menu = ["Create", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    conn = create_connection()
    create_table(conn)
    
    if choice == "Create":
        st.subheader("Input Data")
        varian = st.text("varian rasa minuman")
        name = st.text_input("Nama Peoduk")
        description = st.text_area("Deskripsi")
        
        if st.button("Add"):
            add_project(conn, (varian, name, description))
            st.success(f"Project '{name}' added successfully")
    
    elif choice == "Read":
        st.subheader("View Projects")
        projects = get_projects(conn)
        for project in projects:
            st.write(f"ID: {project[0]} Name: {project[1]} Description: {project[2]}")
    
    elif choice == "Update":
        st.subheader("Edit Project")
        projects = get_projects(conn)
        project_ids = [project[0] for project in projects]
        selected_id = st.selectbox("Select Project ID", project_ids)
        selected_project = next((project for project in projects if project[0] == selected_id), None)
        
        if selected_project:
            name = st.text_input("Project Name", selected_project[1])
            description = st.text_area("Description", selected_project[2])
            
            if st.button("Update"):
                update_project(conn, (name, description, selected_id))
                st.success(f"Project '{name}' updated successfully")
    
    elif choice == "Delete":
        st.subheader("Delete Project")
        projects = get_projects(conn)
        project_ids = [project[0] for project in projects]
        selected_id = st.selectbox("Select Project ID", project_ids)
        
        if st.button("Delete"):
            delete_project(conn, selected_id)
            st.success("Project deleted successfully")

if __name__ == '__main__':
    main()
