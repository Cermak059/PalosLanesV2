package com.example.paloslanesapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;

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


public class SignUpPage extends AppCompatActivity {

    EditText mBday;
    EditText mFname;
    EditText mLname;
    EditText mEmail;
    EditText mPhone;
    EditText mUsername;
    EditText mPassword;
    EditText mConfirm;
    CheckBox mCheckBox;
    Button mSubmit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up_page);

        //Create references to UI
         mFname =  findViewById(R.id.editFname);
         mLname =  findViewById(R.id.editLname);
         mEmail =  findViewById(R.id.editEmail);
         mPhone =  findViewById(R.id.editPhone);
         mBday =  findViewById(R.id.editBirthDate);
         mCheckBox = findViewById(R.id.checkYes);
         mSubmit =  findViewById(R.id.btnSubmit);
         mUsername = findViewById(R.id.editUsername);
         mPassword = findViewById(R.id.editPassword);
         mConfirm = findViewById(R.id.editConfirm);

        //Format text for dates with /
        mBday.addTextChangedListener(new TextWatcher() {

            int beforeLength;

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                beforeLength = mBday.length();
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int count, int after) {
                int dates = mBday.getText().toString().length();
                if (beforeLength < dates && (dates == 2 || dates == 5)) {
                    mBday.append("/");
                }
            }

            @Override
            public void afterTextChanged(Editable s) {}
        });

        //Format text for phone numbers with -
        mPhone.addTextChangedListener(new TextWatcher() {

            int beforeLength;

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                beforeLength = mPhone.length();
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                int digits = mPhone.getText().toString().length();
                if (beforeLength < digits && (digits == 3 || digits == 7)) {
                    mPhone.append("-");
                }
            }

            @Override
            public void afterTextChanged(Editable s) { }
        });

        //Create onClickListener for button submit
        mSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            //Validate text when submit button is clicked
            public void onClick(View view) {
                final String FirstName = mFname.getText().toString();
                final String LastName = mLname.getText().toString();
                final String Email = mEmail.getText().toString();
                final String Phone = mPhone.getText().toString();
                final String Birthday = mBday.getText().toString();
                final String Username = mUsername.getText().toString();
                final String Password = mPassword.getText().toString();
                final String Confirm = mConfirm.getText().toString();


                //validate first name text
                if (FirstName.length()==0) {
                    mFname.requestFocus();
                    mFname.setError("Field cannot be empty");
                }
                else if (FirstName.length()==1) {
                    mFname.requestFocus();
                    mFname.setError("Must be atleast 2 characters");
                }
                else if (!FirstName.matches("[a-zA-Z]+")) {
                    mFname.requestFocus();
                    mFname.setError("Use only alphabetical characters");
                }
                //validate last name text
                else if (LastName.length()==0) {
                    mLname.requestFocus();
                    mLname.setError("Field cannot be empty");
                }
                else if (LastName.length()==1) {
                    mLname.requestFocus();
                    mLname.setError("Must be atleast 2 characters");
                }
                else if (!LastName.matches("[a-zA-Z]+")) {
                    mLname.requestFocus();
                    mLname.setError("Use only alphabetical characters");
                }
                //Validate birthday text
                else if (Birthday.length()!=10) {
                    mBday.requestFocus();
                    mBday.setError("Must us the format 00/00/0000");
                }
                else if (!Birthday.matches("[0-9/]+")) {
                    mBday.requestFocus();
                    mBday.setError("Use only numerical characters");
                }
                //Validate email text
                else if (Email.length()==0) {
                    mEmail.requestFocus();
                    mEmail.setError("Field cannot be empty");
                }
                //Validate phone text
                else if (Phone.length()!=12) {
                    mPhone.requestFocus();
                    mPhone.setError("Must use format 123-123-1234");
                }
                else if (!Phone.matches("[0-9-]+")) {
                    mPhone.requestFocus();
                    mPhone.setError("Use only numerical values");
                }
                //Validate Username text
                else if (Username.length() == 0) {
                    mUsername.requestFocus();
                    mUsername.setError("Field cannot be empty");
                }
                else if (Username.length() == 1) {
                    mUsername.requestFocus();
                    mUsername.setError("Must contain minimum 2 characters");
                }
                else if (!Username.matches("[a-zA-Z0-9]+")) {
                    mUsername.requestFocus();
                    mUsername.setError("Field cannot use special characters");
                }
                //Validate Password text
                else if (Password.length() == 0) {
                    mPassword.requestFocus();
                    mPassword.setError("Field cannot be empty");
                }
                else if (Password.length() < 6) {
                    mPassword.requestFocus();
                    mPassword.setError("Must contain minimum 6 characters");
                }
                //Validate confirm password text
                else if (Confirm.length() == 0) {
                    mConfirm.requestFocus();
                    mConfirm.setError("Field cannot be empty");
                }
                else if (Confirm.length() < 6) {
                    mConfirm.requestFocus();
                    mConfirm.setError("Must contain minimum of 6 characters");
                }
                else if (!Confirm.equals(Password)) {
                    mConfirm.requestFocus();
                    mConfirm.setError("Passwords do not match");
                }
                else {
                    try {
                        postRequest();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        });
    }

    public void postRequest() throws IOException {

        final String FirstName = mFname.getText().toString();
        final String LastName = mLname.getText().toString();
        final String Birthday = mBday.getText().toString();
        final String Email = mEmail.getText().toString();
        final String Phone = mPhone.getText().toString();
        final boolean League = mCheckBox.isChecked();
        final String Username = mUsername.getText().toString();
        final String Password = mPassword.getText().toString();


        MediaType MEDIA_TYPE = MediaType.parse("application/json");
        String url = "http://3.15.199.174:5000/Register";

        OkHttpClient client = new OkHttpClient();

        JSONObject postdata = new JSONObject();
        try {
            postdata.put("Fname", FirstName );
            postdata.put("Lname", LastName );
            postdata.put("Birthdate", Birthday);
            postdata.put("Email", Email);
            postdata.put("Phone", Phone);
            postdata.put("League", League);
            postdata.put("Username", Username);
            postdata.put("Password", Password);
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
            public void onFailure(okhttp3.Call call, IOException e) {
                String mMessage = e.getMessage().toString();
                Log.w("failure Response", mMessage);
                call.cancel();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                final String mMessage = response.body().string();
                if (response.isSuccessful()) {
                    Log.i("", mMessage);
                    SignUpPage.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(SignUpPage.this, mMessage, Toast.LENGTH_LONG).show();
                            //Display toast and call method to switch activity
                            New();
                        }
                    });
                } else {
                    Log.i("", mMessage);
                    SignUpPage.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(SignUpPage.this, mMessage, Toast.LENGTH_LONG).show();
                        }
                    });

                }
            }
        });
    }
    public void New() {
        Intent loginpage = new Intent(this,LoginPage.class);
        startActivity(loginpage);
    }

}
