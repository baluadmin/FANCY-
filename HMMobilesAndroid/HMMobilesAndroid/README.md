# HM Mobiles Android WebView App

This project wraps the existing HM Mobiles Streamlit app in a native Android WebView and uses a desktop Chrome user-agent so the Streamlit wide layout is retained on phones.

## Before building

Open:
`app/src/main/java/com/hmmobiles/app/MainActivity.java`

Replace:
`https://YOUR-STREAMLIT-APP-URL.streamlit.app/`

with the public URL of your deployed Streamlit application.

## Build APK in Android Studio

1. Open this folder in Android Studio.
2. Allow Gradle sync to finish.
3. Select **Build > Build APK(s)**.
4. The debug APK will be under:
`app/build/outputs/apk/debug/app-debug.apk`

## Notes

- The Python/Streamlit app remains the backend/UI source; the APK is the Android WebView shell.
- Your existing Google Sheets requests continue to be handled by the Streamlit/Python app.
- Portrait and landscape are both allowed.
- Back button navigates inside the WebView before exiting.
- If the Streamlit app is not publicly reachable, the APK cannot load it from a phone.
