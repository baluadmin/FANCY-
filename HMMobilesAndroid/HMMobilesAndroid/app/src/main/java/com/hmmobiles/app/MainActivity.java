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

        // Portrait mode
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        // Create WebView
        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();

        // Enable JavaScript
        settings.setJavaScriptEnabled(true);

        // Enable DOM storage for Streamlit
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);

        // WebView settings
        settings.setJavaScriptCanOpenWindowsAutomatically(true);
        settings.setSupportMultipleWindows(true);

        // Mobile-width rendering
        settings.setUseWideViewPort(false);
        settings.setLoadWithOverviewMode(false);

        // Disable zoom
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);

        // Text/rendering
        settings.setDefaultTextEncodingName("UTF-8");
        settings.setTextZoom(100);

        webView.setInitialScale(100);

        // Keep navigation inside the app
        webView.setWebViewClient(new WebViewClient());

        // Support JavaScript dialogs/popups
        webView.setWebChromeClient(new WebChromeClient());

        // Load Bavesh Fancy & Stationery Streamlit website
        webView.loadUrl("https://baveshfancy.streamlit.app/");
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
            webView.stopLoading();
            webView.destroy();
            webView = null;
        }

        super.onDestroy();
    }
}
