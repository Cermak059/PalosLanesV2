package com.example.paloslanesapp;

import androidx.appcompat.app.AppCompatActivity;


import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.util.Log;
import android.widget.Toast;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class LoginPage extends AppCompatActivity {

    EditText mUsername;
    EditText mPassword;
    Button Login;
    CheckBox mCheckbox;
    private SharedPreferences mPreferences;
    private SharedPreferences.Editor mEditor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login_page);

        //Get reference to widgets
        mUsername =  findViewById(R.id.editUserName);
        mPassword =  findViewById(R.id.editPassword);
        mCheckbox =  findViewById(R.id.checkBoxRemember);
        Login =  findViewById(R.id.btnLogin);
        mPreferences = PreferenceManager.getDefaultSharedPreferences(this);
        mEditor = mPreferences.edit();

        checkSharedPreferences();

        Login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final String Username = mUsername.getText().toString();
                final String Password = mPassword.getText().toString();
                if (Username.length() == 0) {
                    mUsername.requestFocus();
                    mUsername.setError("Field cannot be empty");
                } else if (Username.length() == 1) {
                    mUsername.requestFocus();
                    mUsername.setError("Must be atleast 2 characters");
                } else if (!Username.matches("[a-zA-Z0-9]+")) {
                    mUsername.requestFocus();
                    mUsername.setError("Field cannot use special characters");
                } else if (Password.length() == 0) {
                    mPassword.requestFocus();
                    mPassword.setError("Field cannot be empty");
                } else {
                    //Save data when remember me checkbox is checked
                    if (mCheckbox.isChecked()) {
                        mEditor.putString(getString(R.string.CheckboxSave), "True");
                        mEditor.commit();

                        String UsernameSave = mUsername.getText().toString();
                        mEditor.putString(getString(R.string.UsernameSave), UsernameSave);
                        mEditor.commit();

                        String PasswordSave = mPassword.getText().toString();
                        mEditor.putString(getString(R.string.PasswordSave), PasswordSave);
                        mEditor.commit();
                    }
                    //Dont save data when remember me checkbox is not checked
                    else {
                        mEditor.putString(getString(R.string.CheckboxSave), "False");
                        mEditor.commit();

                        mEditor.putString(getString(R.string.UsernameSave), "");
                        mEditor.commit();

                        mEditor.putString(getString(R.string.PasswordSave), "");
                        mEditor.commit();
                    }

                    try {
                        postRequest();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                }

            }
        });
    }

    //Check for shared preferences
    private void checkSharedPreferences () {
        String Checkbox = mPreferences.getString(getString(R.string.CheckboxSave), "False");
        String Username = mPreferences.getString(getString(R.string.UsernameSave), "");
        String Password = mPreferences.getString(getString(R.string.PasswordSave), "");

        //Set text if preferences exist
        mUsername.setText(Username);
        mPassword.setText(Password);

        if (Checkbox.equals("True")){
            mCheckbox.setChecked(true);
        }
        else {
            mCheckbox.setChecked(false);
        }
    }

    public void postRequest() throws IOException {

        final String Username = mUsername.getText().toString();
        final String Password = mPassword.getText().toString();

        MediaType MEDIA_TYPE = MediaType.parse("application/json");
        String url = "http://192.168.1.41:5000/Login";

        OkHttpClient client = new OkHttpClient();

        JSONObject postdata = new JSONObject();
        try {
            postdata.put("Username", Username );
            postdata.put("Password", Password );
        } catch(JSONException e){
            e.printStackTrace();
        }

        RequestBody body = RequestBody.create(MEDIA_TYPE, postdata.toString());

        Request request = new Request.Builder()
                .url(url)
                .post(body)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                String mMessage = e.getMessage().toString();
                Log.w("failure Response", mMessage);
                call.cancel();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                final String mMessage = response.body().string();
                if (response.isSuccessful()) {
                    Log.i("", mMessage);
                    LoginPage.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(LoginPage.this, mMessage, Toast.LENGTH_LONG).show();
                            //Display toast and call method to switch activity
                            New();
                        }
                    });
                } else {
                    Log.i("", mMessage);
                    LoginPage.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(LoginPage.this, mMessage, Toast.LENGTH_LONG).show();
                        }
                    });

                }

                //Display toast and call method to switch activity
                //Toast.makeText(LoginPage.this, "Authentication Successful", Toast.LENGTH_LONG).show();
                //New();
            }
        });
    }

    public void New() {
        Intent homepage = new Intent(this,MainActivity.class);
        startActivity(homepage);
    }
    public void btnRegister (View view) {
        Intent signup = new Intent(this,SignUpPage.class);
        startActivity(signup);
    }

}
