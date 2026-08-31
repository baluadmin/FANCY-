package com.hmmobiles.app;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {

    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Keep phone in portrait
        setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        );

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();

        // JavaScript required by Streamlit
        settings.setJavaScriptEnabled(true);

        // Streamlit storage
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);

        // Streamlit/browser features
        settings.setJavaScriptCanOpenWindowsAutomatically(true);
        settings.setSupportMultipleWindows(true);

        /*
         * IMPORTANT:
         * Do NOT force desktop wide viewport scaling.
         */
        settings.setUseWideViewPort(false);
        settings.setLoadWithOverviewMode(false);

        /*
         * Normal browser-style zoom
         */
        settings.setSupportZoom(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);

        /*
         * Keep links inside the app
         */
        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());

        /*
         * Open your Streamlit application
         */
        webView.loadUrl(
                "https://baluaiproject1.streamlit.app/"
        );
    }

    @Override
    public void onBackPressed() {

        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onDestroy() {

        if (webView != null) {
            webView.destroy();
        }

        super.onDestroy();
    }
}
