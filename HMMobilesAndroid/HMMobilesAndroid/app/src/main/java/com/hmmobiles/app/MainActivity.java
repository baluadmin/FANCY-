package com.hmmobiles.app;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {

    private WebView webView;
    private Handler handler = new Handler();

    private boolean isLandscape = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Start application in PORTRAIT
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();

        // Enable JavaScript
        settings.setJavaScriptEnabled(true);

        // Enable Streamlit storage
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);

        // Streamlit support
        settings.setJavaScriptCanOpenWindowsAutomatically(true);
        settings.setSupportMultipleWindows(true);

        // Desktop-style WebView
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);

        // Zoom
        settings.setSupportZoom(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);

        // Keep website inside app
        webView.setWebViewClient(new WebViewClient());

        // Support website features
        webView.setWebChromeClient(new WebChromeClient());

        // Connect JavaScript with Android
        webView.addJavascriptInterface(
                new AndroidBridge(),
                "AndroidBridge"
        );

        // Keep normal system UI
        webView.setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_LAYOUT_STABLE
        );

        // Open HM Mobiles
        webView.loadUrl(
                "https://baluaiproject1.streamlit.app/"
        );

        // Start checking login status
        startLoginChecker();
    }

    /**
     * Check whether user has logged in.
     */
    private void startLoginChecker() {

        handler.postDelayed(new Runnable() {

            @Override
            public void run() {

                if (webView != null) {

                    webView.evaluateJavascript(
                            "(function() {" +

                            // Login page detection
                            "var text = document.body.innerText || '';" +

                            // Login form is visible
                            "var loginPage = " +
                            "text.includes('Customer Portal Login') || " +
                            "text.includes('Secure Login');" +

                            "if (loginPage) {" +

                            // User is NOT logged in
                            "window.AndroidBridge.userLoggedOut();" +

                            "} else {" +

                            // Login page disappeared
                            // User is logged in
                            "window.AndroidBridge.userLoggedIn();" +

                            "}" +

                            "})();",
                            null
                    );
                }

                // Check again after 1 second
                handler.postDelayed(this, 1000);
            }

        }, 3000);
    }

    /**
     * JavaScript -> Android bridge
     */
    public class AndroidBridge {

        @JavascriptInterface
        public void userLoggedIn() {

            runOnUiThread(new Runnable() {
                @Override
                public void run() {

                    if (!isLandscape) {

                        isLandscape = true;

                        // Change to LANDSCAPE
                        setRequestedOrientation(
                                ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
                        );
                    }
                }
            });
        }

        @JavascriptInterface
        public void userLoggedOut() {

            runOnUiThread(new Runnable() {
                @Override
                public void run() {

                    if (isLandscape) {

                        isLandscape = false;

                        // Return to PORTRAIT
                        setRequestedOrientation(
                                ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
                        );
                    }
                }
            });
        }
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

        handler.removeCallbacksAndMessages(null);

        if (webView != null) {
            webView.destroy();
        }

        super.onDestroy();
    }
}
