import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import plotly.express as px

st.set_page_config(
    page_title="Loan Applications",
    page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxODcuMTk5IiBoZWlnaHQ9IjM1LjM0OCIgdmlld0JveD0iMCAwIDE4Ny4xOTkgMzUuMzQ4Ij4KICA8ZyBpZD0iR3JvdXBfOTI4OCIgZGF0YS1uYW1lPSJHcm91cCA5Mjg4IiB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0NjQyIDQ1MTEuNTExKSI+CiAgICA8ZyBpZD0iR3JvdXBfMSIgZGF0YS1uYW1lPSJHcm91cCAxIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNDY0MiAtNDUxMS41MTEpIj4KICAgICAgPGNpcmNsZSBpZD0iRWxsaXBzZV8xIiBkYXRhLW5hbWU9IkVsbGlwc2UgMSIgY3g9IjUuMzg5IiBjeT0iNS4zODkiIHI9IjUuMzg5IiBmaWxsPSIjMDYwNjFlIi8+CiAgICAgIDxjaXJjbGUgaWQ9IkVsbGlwc2VfMiIgZGF0YS1uYW1lPSJFbGxpcHNlIDIiIGN4PSI1LjM4OSIgY3k9IjUuMzg5IiByPSI1LjM4OSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTIuMikiIGZpbGw9IiMwNjA2MWUiLz4KICAgICAgPGNpcmNsZSBpZD0iRWxsaXBzZV8zIiBkYXRhLW5hbWU9IkVsbGlwc2UgMyIgY3g9IjUuMzg5IiBjeT0iNS4zODkiIHI9IjUuMzg5IiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgyNC40KSIgZmlsbD0iIzA2MDYxZSIvPgogICAgICA8Y2lyY2xlIGlkPSJFbGxpcHNlXzQiIGRhdGEtbmFtZT0iRWxsaXBzZSA0IiBjeD0iNS4zODkiIGN5PSI1LjM4OSIgcj0iNS4zODkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMTIuMjk2KSIgZmlsbD0iIzA2MDYxZSIvPgogICAgICA8Y2lyY2xlIGlkPSJFbGxpcHNlXzUiIGRhdGEtbmFtZT0iRWxsaXBzZSA1IiBjeD0iNS4zODkiIGN5PSI1LjM4OSIgcj0iNS4zODkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDEyLjIgMTIuMjk2KSIgZmlsbD0iIzA2MDYxZSIvPgogICAgICA8Y2lyY2xlIGlkPSJFbGxpcHNlXzYiIGRhdGEtbmFtZT0iRWxsaXBzZSA2IiBjeD0iNS4zODkiIGN5PSI1LjM4OSIgcj0iNS4zODkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMjQuNTcpIiBmaWxsPSIjMDYwNjFlIi8+CiAgICA8L2c+CiAgICA8cGF0aCBpZD0iUGF0aF8zNDc0IiBkYXRhLW5hbWU9IlBhdGggMzQ3NCIgZD0iTTEuNiwwVi0yMC4zSDE2LjU4OHY0LjAzMUg1Ljk0NXY0LjE0N2g5LjQ4M3YzLjkxNUg1Ljk0NVYwWk0xOS4yLDBWLTE1LjM3aDQuMlYwWm0uMzE5LTIwLjg1MWEyLjUzOSwyLjUzOSwwLDAsMSwxLjgyNy0uNzI1LDIuNTM5LDIuNTM5LDAsMCwxLDEuODI3LjcyNSwyLjM2MSwyLjM2MSwwLDAsMSwuNzU0LDEuNzY5LDIuMzE1LDIuMzE1LDAsMCwxLS43NTQsMS43NTQsMi41NjcsMi41NjcsMCwwLDEtMS44MjcuNzExLDIuNTY3LDIuNTY3LDAsMCwxLTEuODI3LS43MTEsMi4zMTUsMi4zMTUsMCwwLDEtLjc1NC0xLjc1NEEyLjM2MSwyLjM2MSwwLDAsMSwxOS41MTctMjAuODUxWm02LjkzMSw1LjQ4MWg0LjJ2MS40MjFhNS42NzksNS42NzksMCwwLDEsMS44Ny0xLjIzMyw2LjI4Myw2LjI4MywwLDAsMSwyLjQyMi0uNDQ5LDYuODgzLDYuODgzLDAsMCwxLDMuMTQ2Ljc0QTUuODcyLDUuODcyLDAsMCwxLDQwLjQ0LTEyLjc2YTUuODcyLDUuODcyLDAsMCwxLC44ODUsMy4yMTlWMEgzNy4xMlYtOC40NjhhMy40NjcsMy40NjcsMCwwLDAtLjQwNi0xLjcsMi45MjQsMi45MjQsMCwwLDAtMS4xLTEuMTQ2LDMsMywwLDAsMC0xLjUzNy0uNDA2LDMuMjMyLDMuMjMyLDAsMCwwLTEuOC41MDgsMy4zNTUsMy4zNTUsMCwwLDAtMS4yLDEuMzYzLDQuMjQ3LDQuMjQ3LDAsMCwwLS40MiwxLjlWMGgtNC4yWm0xNy4yLDcuNjg1YTcuNzYsNy43NiwwLDAsMSwxLjA3My00LDcuOTA3LDcuOTA3LDAsMCwxLDIuOS0yLjg4NSw3LjczNCw3LjczNCwwLDAsMSwzLjk0NC0xLjA1OEE3LjUxMSw3LjUxMSwwLDAsMSw1Ni0xNC4yMzlhNy44MDcsNy44MDcsMCwwLDEsMi44NDIsMy42NTRsLTMuODI4LDEuMWE0LjA0OCw0LjA0OCwwLDAsMC0xLjM3Ny0xLjcyNiwzLjQ3OSwzLjQ3OSwwLDAsMC0yLjA3NC0uNjUzLDMuNjg0LDMuNjg0LDAsMCwwLTIuMDE1LjU4QTQuMjU2LDQuMjU2LDAsMCwwLDQ4LjEtOS43NDRhNC4xNDMsNC4xNDMsMCwwLDAtLjUzNiwyLjA1OUE0LjE0Myw0LjE0MywwLDAsMCw0OC4xLTUuNjI2LDQuMTM4LDQuMTM4LDAsMCwwLDQ5LjU0Ny00LjFhMy43NTQsMy43NTQsMCwwLDAsMi4wMTUuNTY1LDMuNDYxLDMuNDYxLDAsMCwwLDIuMDg4LS42NTMsNC4xMjUsNC4xMjUsMCwwLDAsMS4zNjMtMS43bDMuODI4LDEuMUE3Ljg1OSw3Ljg1OSwwLDAsMSw1Ni4wMTQtMS4xNiw3LjQ5Miw3LjQ5MiwwLDAsMSw1MS41NjIuMjMyYTcuNzYsNy43NiwwLDAsMS00LTEuMDczLDcuOCw3LjgsMCwwLDEtMi44NzEtMi45QTcuODE3LDcuODE3LDAsMCwxLDQzLjY0NS03LjY4NVpNNjEuMjE5LTIwLjNoNC4yMDVWMEg2MS4yMTlabTExLjMxLDQuOTNWLTYuOWEzLjQ2NywzLjQ2NywwLDAsMCwuNDA2LDEuNywyLjkyNCwyLjkyNCwwLDAsMCwxLjEsMS4xNDYsMywzLDAsMCwwLDEuNTM3LjQwNiwzLjIzMiwzLjIzMiwwLDAsMCwxLjgtLjUwNywzLjM1NSwzLjM1NSwwLDAsMCwxLjItMS4zNjNBNC4yNDcsNC4yNDcsMCwwLDAsNzktNy40MjRWLTE1LjM3SDgzLjJWMEg3OVYtMS40MjFhNS42OCw1LjY4LDAsMCwxLTEuODcsMS4yMzNBNi4yODMsNi4yODMsMCwwLDEsNzQuNy4yNjFhNi44ODMsNi44ODMsMCwwLDEtMy4xNDYtLjczOUE1Ljg3Miw1Ljg3MiwwLDAsMSw2OS4yMDktMi42MWE1Ljg3Miw1Ljg3MiwwLDAsMS0uODg1LTMuMjE5Vi0xNS4zN1ptMTMuMjgyLDQuNTI0YTQuMTcsNC4xNywwLDAsMSwuODEyLTIuNTY2LDUuMDEyLDUuMDEyLDAsMCwxLDIuMjYyLTEuNjUzLDkuMTM0LDkuMTM0LDAsMCwxLDMuMzM1LS41NjUsMTMuMjc5LDEzLjI3OSwwLDAsMSwzLjE0Ni4zNzcsMTIuMTE4LDEyLjExOCwwLDAsMSwyLjc3LDEuMDE1djMuOTczYTE5LjM2MSwxOS4zNjEsMCwwLDAtMy40OTUtMS4zOTIsOS44MzQsOS44MzQsMCwwLDAtMi40MjEtLjM3NywzLjUsMy41LDAsMCwwLTEuMTMxLjE2LDEuNjEyLDEuNjEyLDAsMCwwLS43LjQyLjg1My44NTMsMCwwLDAtLjIzMi41OC44MzkuODM5LDAsMCwwLC41OC43ODMsOS42MTIsOS42MTIsMCwwLDAsMS45MTQuNTIycS4zNDguMDg3LjcxLjE2YTcuNTUyLDcuNTUyLDAsMCwxLC43NC4xODgsNy44ODMsNy44ODMsMCwwLDEsMy42NTQsMS44NTYsNC4wMzIsNC4wMzIsMCwwLDEsMS4xNiwyLjkyOUEzLjgsMy44LDAsMCwxLDk2Ljk5LS44N2E4Ljg3Myw4Ljg3MywwLDAsMS00LjQ4LDEuMSwxMS43NzksMTEuNzc5LDAsMCwxLTMuMDE2LS40MDYsMTMuODcyLDEzLjg3MiwwLDAsMS0zLjE2MS0xLjNWLTUuNjU1YTE1LjUyMSwxNS41MjEsMCwwLDAsMi44ODUsMS41MDgsOC42NDcsOC42NDcsMCwwLDAsMy4yOTEuNzI1LDQuNzUyLDQuNzUyLDAsMCwwLDEuMDE1LS4xLDEuODE4LDEuODE4LDAsMCwwLC43NjktLjM0OC44LjgsMCwwLDAsLjMtLjY1M3EwLS42MDktLjgxMi0uOTcxYTE1LjA3MywxNS4wNzMsMCwwLDAtMi43MjYtLjc2OCw5LjIyMSw5LjIyMSwwLDAsMS0zLjk3My0xLjY1M0EzLjYyNSwzLjYyNSwwLDAsMSw4NS44MTEtMTAuODQ2Wk0xMDEuMDk0LDBWLTE1LjM3SDEwNS4zVjBabS4zMTktMjAuODUxYTIuNTM5LDIuNTM5LDAsMCwxLDEuODI3LS43MjUsMi41MzksMi41MzksMCwwLDEsMS44MjcuNzI1LDIuMzYxLDIuMzYxLDAsMCwxLC43NTQsMS43NjksMi4zMTUsMi4zMTUsMCwwLDEtLjc1NCwxLjc1NCwyLjU2NywyLjU2NywwLDAsMS0xLjgyNy43MTEsMi41NjcsMi41NjcsMCwwLDEtMS44MjctLjcxMSwyLjMxNSwyLjMxNSwwLDAsMS0uNzU0LTEuNzU0QTIuMzYxLDIuMzYxLDAsMCwxLDEwMS40MTMtMjAuODUxWm02LjQwOSwxMy4xMzdhNy42Myw3LjYzLDAsMCwxLDEuMDczLTMuOTU4LDguMDkyLDguMDkyLDAsMCwxLDIuODg1LTIuODg1LDcuNjMsNy42MywwLDAsMSwzLjk1OS0xLjA3Myw3LjYzLDcuNjMsMCwwLDEsMy45NTgsMS4wNzMsOC4wNTYsOC4wNTYsMCwwLDEsMi44ODYsMi45LDcuNjU0LDcuNjU0LDAsMCwxLDEuMDczLDMuOTQ0LDcuNzA3LDcuNzA3LDAsMCwxLTEuMDczLDMuOTczLDguMDU2LDguMDU2LDAsMCwxLTIuODg2LDIuOUE3LjYzLDcuNjMsMCwwLDEsMTE1LjczOS4yMzIsNy41NTMsNy41NTMsMCwwLDEsMTExLjc4LS44NTVhOC4xNzMsOC4xNzMsMCwwLDEtMi44ODUtMi45MTRBNy42NTQsNy42NTQsMCwwLDEsMTA3LjgyMi03LjcxNFptMy45MTUsMGE0LjA2Myw0LjA2MywwLDAsMCwuNTM2LDIuMDQ1LDQuMTcyLDQuMTcyLDAsMCwwLDEuNDUsMS41MDgsMy43NTQsMy43NTQsMCwwLDAsMi4wMTYuNTY2LDMuNzU0LDMuNzU0LDAsMCwwLDIuMDE2LS41NjYsNC4xNzIsNC4xNzIsMCwwLDAsMS40NS0xLjUwOCw0LjA2Myw0LjA2MywwLDAsMCwuNTM2LTIuMDQ1LDQuMDYzLDQuMDYzLDAsMCwwLS41MzYtMi4wNDQsNC4wNTYsNC4wNTYsMCwwLDAtMS40NS0xLjQ5NCwzLjgyOCwzLjgyOCwwLDAsMC0yLjAxNi0uNTUxLDMuNzU0LDMuNzU0LDAsMCwwLTIuMDE2LjU2Niw0LjIwOCw0LjIwOCwwLDAsMC0xLjQ1LDEuNDkzQTMuOTg1LDMuOTg1LDAsMCwwLDExMS43MzctNy43MTRabTE0LjMtNy42NTZoNC4yMDV2MS40MjFhNS42OCw1LjY4LDAsMCwxLDEuODctMS4yMzMsNi4yODMsNi4yODMsMCwwLDEsMi40MjItLjQ0OSw2Ljg4Myw2Ljg4MywwLDAsMSwzLjE0Ni43NCw1Ljg3Miw1Ljg3MiwwLDAsMSwyLjM0OSwyLjEzMSw1Ljg3Miw1Ljg3MiwwLDAsMSwuODg0LDMuMjE5VjBoLTQuMjA1Vi04LjQ2OGEzLjQ2NywzLjQ2NywwLDAsMC0uNDA2LTEuNywyLjkyNCwyLjkyNCwwLDAsMC0xLjEtMS4xNDYsMywzLDAsMCwwLTEuNTM3LS40MDYsMy4yMzIsMy4yMzIsMCwwLDAtMS44LjUwOCwzLjM1NSwzLjM1NSwwLDAsMC0xLjIsMS4zNjMsNC4yNDcsNC4yNDcsMCwwLDAtLjQyMSwxLjlWMGgtNC4yMDVaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNDU5NS43MTIgLTQ0ODMuNTM3KSIgZmlsbD0iIzA2MDYxZSIvPgogIDwvZz4KPC9zdmc+Cg==",
    layout="wide"
)

# Header
st.image("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxODcuMTk5IiBoZWlnaHQ9IjM1LjM0OCIgdmlld0JveD0iMCAwIDE4Ny4xOTkgMzUuMzQ4Ij4KICA8ZyBpZD0iR3JvdXBfOTI4OCIgZGF0YS1uYW1lPSJHcm91cCA5Mjg4IiB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0NjQyIDQ1MTEuNTExKSI+CiAgICA8ZyBpZD0iR3JvdXBfMSIgZGF0YS1uYW1lPSJHcm91cCAxIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNDY0MiAtNDUxMS41MTEpIj4KICAgICAgPGNpcmNsZSBpZD0iRWxsaXBzZV8xIiBkYXRhLW5hbWU9IkVsbGlwc2UgMSIgY3g9IjUuMzg5IiBjeT0iNS4zODkiIHI9IjUuMzg5IiBmaWxsPSIjMDYwNjFlIi8+CiAgICAgIDxjaXJjbGUgaWQ9IkVsbGlwc2VfMiIgZGF0YS1uYW1lPSJFbGxpcHNlIDIiIGN4PSI1LjM4OSIgY3k9IjUuMzg5IiByPSI1LjM4OSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTIuMikiIGZpbGw9IiMwNjA2MWUiLz4KICAgICAgPGNpcmNsZSBpZD0iRWxsaXBzZV8zIiBkYXRhLW5hbWU9IkVsbGlwc2UgMyIgY3g9IjUuMzg5IiBjeT0iNS4zODkiIHI9IjUuMzg5IiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgyNC40KSIgZmlsbD0iIzA2MDYxZSIvPgogICAgICA8Y2lyY2xlIGlkPSJFbGxpcHNlXzQiIGRhdGEtbmFtZT0iRWxsaXBzZSA0IiBjeD0iNS4zODkiIGN5PSI1LjM4OSIgcj0iNS4zODkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMTIuMjk2KSIgZmlsbD0iIzA2MDYxZSIvPgogICAgICA8Y2lyY2xlIGlkPSJFbGxpcHNlXzUiIGRhdGEtbmFtZT0iRWxsaXBzZSA1IiBjeD0iNS4zODkiIGN5PSI1LjM4OSIgcj0iNS4zODkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDEyLjIgMTIuMjk2KSIgZmlsbD0iIzA2MDYxZSIvPgogICAgICA8Y2lyY2xlIGlkPSJFbGxpcHNlXzYiIGRhdGEtbmFtZT0iRWxsaXBzZSA2IiBjeD0iNS4zODkiIGN5PSI1LjM4OSIgcj0iNS4zODkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMjQuNTcpIiBmaWxsPSIjMDYwNjFlIi8+CiAgICA8L2c+CiAgICA8cGF0aCBpZD0iUGF0aF8zNDc0IiBkYXRhLW5hbWU9IlBhdGggMzQ3NCIgZD0iTTEuNiwwVi0yMC4zSDE2LjU4OHY0LjAzMUg1Ljk0NXY0LjE0N2g5LjQ4M3YzLjkxNUg1Ljk0NVYwWk0xOS4yLDBWLTE1LjM3aDQuMlYwWm0uMzE5LTIwLjg1MWEyLjUzOSwyLjUzOSwwLDAsMSwxLjgyNy0uNzI1LDIuNTM5LDIuNTM5LDAsMCwxLDEuODI3LjcyNSwyLjM2MSwyLjM2MSwwLDAsMSwuNzU0LDEuNzY5LDIuMzE1LDIuMzE1LDAsMCwxLS43NTQsMS43NTQsMi41NjcsMi41NjcsMCwwLDEtMS44MjcuNzExLDIuNTY3LDIuNTY3LDAsMCwxLTEuODI3LS43MTEsMi4zMTUsMi4zMTUsMCwwLDEtLjc1NC0xLjc1NEEyLjM2MSwyLjM2MSwwLDAsMSwxOS41MTctMjAuODUxWm02LjkzMSw1LjQ4MWg0LjJ2MS40MjFhNS42NzksNS42NzksMCwwLDEsMS44Ny0xLjIzMyw2LjI4Myw2LjI4MywwLDAsMSwyLjQyMi0uNDQ5LDYuODgzLDYuODgzLDAsMCwxLDMuMTQ2Ljc0QTUuODcyLDUuODcyLDAsMCwxLDQwLjQ0LTEyLjc2YTUuODcyLDUuODcyLDAsMCwxLC44ODUsMy4yMTlWMEgzNy4xMlYtOC40NjhhMy40NjcsMy40NjcsMCwwLDAtLjQwNi0xLjcsMi45MjQsMi45MjQsMCwwLDAtMS4xLTEuMTQ2LDMsMywwLDAsMC0xLjUzNy0uNDA2LDMuMjMyLDMuMjMyLDAsMCwwLTEuOC41MDgsMy4zNTUsMy4zNTUsMCwwLDAtMS4yLDEuMzYzLDQuMjQ3LDQuMjQ3LDAsMCwwLS40MiwxLjlWMGgtNC4yWm0xNy4yLDcuNjg1YTcuNzYsNy43NiwwLDAsMSwxLjA3My00LDcuOTA3LDcuOTA3LDAsMCwxLDIuOS0yLjg4NSw3LjczNCw3LjczNCwwLDAsMSwzLjk0NC0xLjA1OEE3LjUxMSw3LjUxMSwwLDAsMSw1Ni0xNC4yMzlhNy44MDcsNy44MDcsMCwwLDEsMi44NDIsMy42NTRsLTMuODI4LDEuMWE0LjA0OCw0LjA0OCwwLDAsMC0xLjM3Ny0xLjcyNiwzLjQ3OSwzLjQ3OSwwLDAsMC0yLjA3NC0uNjUzLDMuNjg0LDMuNjg0LDAsMCwwLTIuMDE1LjU4QTQuMjU2LDQuMjU2LDAsMCwwLDQ4LjEtOS43NDRhNC4xNDMsNC4xNDMsMCwwLDAtLjUzNiwyLjA1OUE0LjE0Myw0LjE0MywwLDAsMCw0OC4xLTUuNjI2LDQuMTM4LDQuMTM4LDAsMCwwLDQ5LjU0Ny00LjFhMy43NTQsMy43NTQsMCwwLDAsMi4wMTUuNTY1LDMuNDYxLDMuNDYxLDAsMCwwLDIuMDg4LS42NTMsNC4xMjUsNC4xMjUsMCwwLDAsMS4zNjMtMS43bDMuODI4LDEuMUE3Ljg1OSw3Ljg1OSwwLDAsMSw1Ni4wMTQtMS4xNiw3LjQ5Miw3LjQ5MiwwLDAsMSw1MS41NjIuMjMyYTcuNzYsNy43NiwwLDAsMS00LTEuMDczLDcuOCw3LjgsMCwwLDEtMi44NzEtMi45QTcuODE3LDcuODE3LDAsMCwxLDQzLjY0NS03LjY4NVpNNjEuMjE5LTIwLjNoNC4yMDVWMEg2MS4yMTlabTExLjMxLDQuOTNWLTYuOWEzLjQ2NywzLjQ2NywwLDAsMCwuNDA2LDEuNywyLjkyNCwyLjkyNCwwLDAsMCwxLjEsMS4xNDYsMywzLDAsMCwwLDEuNTM3LjQwNiwzLjIzMiwzLjIzMiwwLDAsMCwxLjgtLjUwNywzLjM1NSwzLjM1NSwwLDAsMCwxLjItMS4zNjNBNC4yNDcsNC4yNDcsMCwwLDAsNzktNy40MjRWLTE1LjM3SDgzLjJWMEg3OVYtMS40MjFhNS42OCw1LjY4LDAsMCwxLTEuODcsMS4yMzNBNi4yODMsNi4yODMsMCwwLDEsNzQuNy4yNjFhNi44ODMsNi44ODMsMCwwLDEtMy4xNDYtLjczOUE1Ljg3Miw1Ljg3MiwwLDAsMSw2OS4yMDktMi42MWE1Ljg3Miw1Ljg3MiwwLDAsMS0uODg1LTMuMjE5Vi0xNS4zN1ptMTMuMjgyLDQuNTI0YTQuMTcsNC4xNywwLDAsMSwuODEyLTIuNTY2LDUuMDEyLDUuMDEyLDAsMCwxLDIuMjYyLTEuNjUzLDkuMTM0LDkuMTM0LDAsMCwxLDMuMzM1LS41NjUsMTMuMjc5LDEzLjI3OSwwLDAsMSwzLjE0Ni4zNzcsMTIuMTE4LDEyLjExOCwwLDAsMSwyLjc3LDEuMDE1djMuOTczYTE5LjM2MSwxOS4zNjEsMCwwLDAtMy40OTUtMS4zOTIsOS44MzQsOS44MzQsMCwwLDAtMi40MjEtLjM3NywzLjUsMy41LDAsMCwwLTEuMTMxLjE2LDEuNjEyLDEuNjEyLDAsMCwwLS43LjQyLjg1My44NTMsMCwwLDAtLjIzMi41OC44MzkuODM5LDAsMCwwLC41OC43ODMsOS42MTIsOS42MTIsMCwwLDAsMS45MTQuNTIycS4zNDguMDg3LjcxLjE2YTcuNTUyLDcuNTUyLDAsMCwxLC43NC4xODgsNy44ODMsNy44ODMsMCwwLDEsMy42NTQsMS44NTYsNC4wMzIsNC4wMzIsMCwwLDEsMS4xNiwyLjkyOUEzLjgsMy44LDAsMCwxLDk2Ljk5LS44N2E4Ljg3Myw4Ljg3MywwLDAsMS00LjQ4LDEuMSwxMS43NzksMTEuNzc5LDAsMCwxLTMuMDE2LS40MDYsMTMuODcyLDEzLjg3MiwwLDAsMS0zLjE2MS0xLjNWLTUuNjU1YTE1LjUyMSwxNS41MjEsMCwwLDAsMi44ODUsMS41MDgsOC42NDcsOC42NDcsMCwwLDAsMy4yOTEuNzI1LDQuNzUyLDQuNzUyLDAsMCwwLDEuMDE1LS4xLDEuODE4LDEuODE4LDAsMCwwLC43NjktLjM0OC44LjgsMCwwLDAsLjMtLjY1M3EwLS42MDktLjgxMi0uOTcxYTE1LjA3MywxNS4wNzMsMCwwLDAtMi43MjYtLjc2OCw5LjIyMSw5LjIyMSwwLDAsMS0zLjk3My0xLjY1M0EzLjYyNSwzLjYyNSwwLDAsMSw4NS44MTEtMTAuODQ2Wk0xMDEuMDk0LDBWLTE1LjM3SDEwNS4zVjBabS4zMTktMjAuODUxYTIuNTM5LDIuNTM5LDAsMCwxLDEuODI3LS43MjUsMi41MzksMi41MzksMCwwLDEsMS44MjcuNzI1LDIuMzYxLDIuMzYxLDAsMCwxLC43NTQsMS43NjksMi4zMTUsMi4zMTUsMCwwLDEtLjc1NCwxLjc1NCwyLjU2NywyLjU2NywwLDAsMS0xLjgyNy43MTEsMi41NjcsMi41NjcsMCwwLDEtMS44MjctLjcxMSwyLjMxNSwyLjMxNSwwLDAsMS0uNzU0LTEuNzU0QTIuMzYxLDIuMzYxLDAsMCwxLDEwMS40MTMtMjAuODUxWm02LjQwOSwxMy4xMzdhNy42Myw3LjYzLDAsMCwxLDEuMDczLTMuOTU4LDguMDkyLDguMDkyLDAsMCwxLDIuODg1LTIuODg1LDcuNjMsNy42MywwLDAsMSwzLjk1OS0xLjA3Myw3LjYzLDcuNjMsMCwwLDEsMy45NTgsMS4wNzMsOC4wNTYsOC4wNTYsMCwwLDEsMi44ODYsMi45LDcuNjU0LDcuNjU0LDAsMCwxLDEuMDczLDMuOTQ0LDcuNzA3LDcuNzA3LDAsMCwxLTEuMDczLDMuOTczLDguMDU2LDguMDU2LDAsMCwxLTIuODg2LDIuOUE3LjYzLDcuNjMsMCwwLDEsMTE1LjczOS4yMzIsNy41NTMsNy41NTMsMCwwLDEsMTExLjc4LS44NTVhOC4xNzMsOC4xNzMsMCwwLDEtMi44ODUtMi45MTRBNy42NTQsNy42NTQsMCwwLDEsMTA3LjgyMi03LjcxNFptMy45MTUsMGE0LjA2Myw0LjA2MywwLDAsMCwuNTM2LDIuMDQ1LDQuMTcyLDQuMTcyLDAsMCwwLDEuNDUsMS41MDgsMy43NTQsMy43NTQsMCwwLDAsMi4wMTYuNTY2LDMuNzU0LDMuNzU0LDAsMCwwLDIuMDE2LS41NjYsNC4xNzIsNC4xNzIsMCwwLDAsMS40NS0xLjUwOCw0LjA2Myw0LjA2MywwLDAsMCwuNTM2LTIuMDQ1LDQuMDYzLDQuMDYzLDAsMCwwLS41MzYtMi4wNDQsNC4wNTYsNC4wNTYsMCwwLDAtMS40NS0xLjQ5NCwzLjgyOCwzLjgyOCwwLDAsMC0yLjAxNi0uNTUxLDMuNzU0LDMuNzU0LDAsMCwwLTIuMDE2LjU2Niw0LjIwOCw0LjIwOCwwLDAsMC0xLjQ1LDEuNDkzQTMuOTg1LDMuOTg1LDAsMCwwLDExMS43MzctNy43MTRabTE0LjMtNy42NTZoNC4yMDV2MS40MjFhNS42OCw1LjY4LDAsMCwxLDEuODctMS4yMzMsNi4yODMsNi4yODMsMCwwLDEsMi40MjItLjQ0OSw2Ljg4Myw2Ljg4MywwLDAsMSwzLjE0Ni43NCw1Ljg3Miw1Ljg3MiwwLDAsMSwyLjM0OSwyLjEzMSw1Ljg3Miw1Ljg3MiwwLDAsMSwuODg0LDMuMjE5VjBoLTQuMjA1Vi04LjQ2OGEzLjQ2NywzLjQ2NywwLDAsMC0uNDA2LTEuNywyLjkyNCwyLjkyNCwwLDAsMC0xLjEtMS4xNDYsMywzLDAsMCwwLTEuNTM3LS40MDYsMy4yMzIsMy4yMzIsMCwwLDAtMS44LjUwOCwzLjM1NSwzLjM1NSwwLDAsMC0xLjIsMS4zNjMsNC4yNDcsNC4yNDcsMCwwLDAtLjQyMSwxLjlWMGgtNC4yMDVaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNDU5NS43MTIgLTQ0ODMuNTM3KSIgZmlsbD0iIzA2MDYxZSIvPgogIDwvZz4KPC9zdmc+Cg==")
st.write("### Loan Applications")

# CONNECTION
connection_string = ('DRIVER={SQL Server};'
                    'SERVER=LAPTOP-ABPOUMCR\SQLEXPRESS;'
                    'DATABASE=FinTables')
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)
connection = engine.raw_connection()
myCursor = connection.cursor()

# FUNCTIONS
def AcceptedCount():
    st.write("##### All Loans")
    # get count from sql
    accepted = pd.read_sql("SELECT COUNT(*) AS [Approved] FROM dbo.LoanApplications WHERE AutoApproved = 1", engine)._get_value(0, "Approved")
    declined = pd.read_sql("SELECT COUNT(*) AS [Declined] FROM dbo.LoanApplications WHERE AutoApproved = 0", engine)._get_value(0, "Declined")
    acceptedVal = pd.read_sql("SELECT SUM(Amount) AS Total FROM dbo.LoanApplications WHERE AutoApproved = 1", engine)._get_value(0, "Total")
    declinedVal = pd.read_sql("SELECT SUM(Amount) AS Total FROM dbo.LoanApplications WHERE AutoApproved = 0", engine)._get_value(0, "Total")

    Accept_Decline(accepted, declined, acceptedVal, declinedVal)
    return

def LoanCounts():
    st.write("##### Filtered Loans")

    disp_interval = st.selectbox("Display loans for", ("2021", "2022"))
    if disp_interval == "2021":
        filterBy = "CreateDate BETWEEN '2021' AND '2022'"
    elif disp_interval == "2022":
        filterBy = "CreateDate > '2022'"

    if st.checkbox("Monthly Loans"):
        disp_month = st.selectbox(
            "Select month to display",
            ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
            )
        monthFilter = filterMonth(disp_interval, disp_month)
    else:
        monthFilter = ""
        
    sql = "SELECT * FROM dbo.LoanApplications WHERE " + filterBy + monthFilter + " ORDER BY CreateDate"
    st.write(sql)

    # data from table
    data = pd.read_sql("SELECT * FROM dbo.LoanApplications WHERE " + filterBy + monthFilter + " ORDER BY CreateDate", engine)
    accepted = pd.read_sql("SELECT COUNT(*) AS [Approved] FROM dbo.LoanApplications WHERE " + filterBy + monthFilter + " AND AutoApproved = 1", engine)._get_value(0, "Approved")
    declined = pd.read_sql("SELECT COUNT(*) AS [Declined] FROM dbo.LoanApplications WHERE " + filterBy + monthFilter + " AND AutoApproved = 0", engine)._get_value(0, "Declined")
    acceptedVal = pd.read_sql("SELECT SUM(Amount) AS Total FROM dbo.LoanApplications WHERE " + filterBy + monthFilter + " AND AutoApproved = 1", engine)._get_value(0, "Total")
    declinedVal = pd.read_sql("SELECT SUM(Amount) AS Total FROM dbo.LoanApplications WHERE " + filterBy + monthFilter + " AND AutoApproved = 0", engine)._get_value(0, "Total")
    
    Accept_Decline(accepted, declined, acceptedVal, declinedVal)
      
    # Display table  
    if st.checkbox("Show Table"): 
        st.write(data)

    # Download filtered table
    dataDownload = data.to_parquet()
    st.download_button("Download", dataDownload, "loanApplications.gzip", key="download-csv") 

def filterMonth(disp_interval, disp_month):
    if disp_month == "January":
        filterMonth = " AND CreateDate BETWEEN '" + disp_interval + "-01-01' AND '" + disp_interval + "-02-01'"
    elif disp_month == "February":
        filterMonth = " AND CreateDate BETWEEN '" + disp_interval + "-02-01' AND '" + disp_interval + "-03-01'"
    elif disp_month == "March":
        filterMonth = " AND CreateDate BETWEEN '" + disp_interval + "-03-01' AND '" + disp_interval + "-04-01'"
    elif disp_month == "April":
        filterMonth = " AND CreateDate BETWEEN '" + disp_interval + "-04-01' AND '" + disp_interval + "-05-01'"
    elif disp_month == "May":
        filterMonth = " AND CreateDate BETWEEN '" + disp_interval + "-05-01' AND '" + disp_interval + "-06-01'"
    elif disp_month == "June":
        filterMonth = " AND CreateDate BETWEEN '" + disp_interval + "-06-01' AND '" + disp_interval + "-07-01'"
    elif disp_month == "July":
        filterMonth = " AND CreateDate BETWEEN '" + disp_interval + "-07-01' AND '" + disp_interval + "-08-01'"
    elif disp_month == "August":
        filterMonth = " AND CreateDate BETWEEN '" + disp_interval + "-08-01' AND '" + disp_interval + "-09-01'"
    elif disp_month == "September":
        filterMonth = " AND CreateDate BETWEEN '" + disp_interval + "-09-01' AND '" + disp_interval + "-10-01'"
    elif disp_month == "October":
        filterMonth = " AND CreateDate BETWEEN '" + disp_interval + "-10-01' AND '" + disp_interval + "-11-01'"
    elif disp_month == "November":
        filterMonth = " AND CreateDate BETWEEN '" + disp_interval + "-11-01' AND '" + disp_interval + "-12-01'"
    elif disp_month == "December":
        filterMonth = " AND CreateDate > '" + disp_interval + "-12-01'"
    return filterMonth

def Accept_Decline(accepted, declined, acceptedVal, declinedVal):
    col1, col2, col3 = st.columns(3)
    accept_decline = pd.DataFrame([accepted, declined], index=["Approved", "Declined"])
    accept_declineVal = pd.DataFrame([acceptedVal, declinedVal], index=["Approved", "Declined"])

    with col1:
        st.write("##### Loans approved")
        st.write(str(accepted))
        st.write("##### Loans declined")
        st.write(str(declined))

        st.write("##### Approved Value")
        st.write("R" + str(acceptedVal))
        st.write("##### Declined Value")
        st.write("R" + str(declinedVal))
    
    with col2:
        fig = px.bar(
                accept_decline,
                title="Loans Given"
            )
        fig.update_layout(width=400, height=300)
        st.write(fig)
    
    with col3:
        fig = px.bar(
                accept_declineVal,
                title="Loan Values"
            )
        fig.update_layout(width=400, height=300)
        st.write(fig)

def DisplayFile():
    st.write("##### Updload File")
    uploadedFile = st.file_uploader("Select file")

    if st.button("Show file"):
        file = pd.read_parquet(uploadedFile)
        st.write(file)

# BEGIN 
with st.sidebar:
    display = st.selectbox(
        "Display",
        ("Loan Information", "Filter Loans", "Upload file to display")
    )
if display == "Loan Information":
    AcceptedCount()
elif display == "Filter Loans":
    LoanCounts()
elif display == "Upload file to display":
    DisplayFile()
# END