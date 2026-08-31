package com.hmmobiles.app;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {

    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();

        // Enable JavaScript
        settings.setJavaScriptEnabled(true);

        // Enable storage for Streamlit
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);

        // Allow Streamlit features
        settings.setJavaScriptCanOpenWindowsAutomatically(true);
        settings.setSupportMultipleWindows(true);

        // MOBILE VIEW
        // Do NOT force a desktop/wide page
        settings.setUseWideViewPort(false);
        settings.setLoadWithOverviewMode(false);

        // Normal phone zoom
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);

        // Keep website inside the app
        webView.setWebViewClient(new WebViewClient());

        // Support Streamlit browser features
        webView.setWebChromeClient(new WebChromeClient());

        // Normal screen layout
        webView.setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_LAYOUT_STABLE
        );

        // Open HM Mobiles
        webView.loadUrl("https://baluaiproject1.streamlit.app/");
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
