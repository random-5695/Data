from github import Github
import streamlit as st

ACCESS_TOKEN = "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"
GITHUB_REPO = "data"
GIT_BRANCH = "main"
INTERNAL_FILE = "output/TechCrunch.json"
FOLDER_EMPL_IN_GIT = "TechCrunch.json"

st.divider()

st.subheader("Export the JSON File to Github Repo: ")

if st.button("Export", type="primary") :
    
    def add_or_update_in_git(access_tocken, github_repo, git_branch, initial_file, folder_empl_in_git):
        g = Github(access_tocken)

        repo = g.get_user().get_repo(github_repo)

        all_files = []
        contents = repo.get_contents("")

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                file = file_content
                all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

        with open(initial_file, 'r') as file:
            content = file.read()

        # Upload to github
        if folder_empl_in_git in all_files:
            contents = repo.get_contents(folder_empl_in_git)
            repo.update_file(contents.path, "committing files", content, contents.sha, branch=git_branch)
            return folder_empl_in_git + ' UPDATED'
        else:
            repo.create_file(folder_empl_in_git, "committing files", content, branch=git_branch)
            return folder_empl_in_git + ' CREATED'


    add_or_update_in_git(ACCESS_TOKEN, GITHUB_REPO, GIT_BRANCH, INTERNAL_FILE, FOLDER_EMPL_IN_GIT)

else:
    st.error("Error!!!")