package com.example.paloslanesapp;

import androidx.appcompat.app.AppCompatActivity;


import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.widget.Toast;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;

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
        mUsername = (EditText) findViewById(R.id.editUserName);
        mPassword = (EditText) findViewById(R.id.editPassword);
        mCheckbox = (CheckBox) findViewById(R.id.checkBoxRemember);
        Login = (Button) findViewById(R.id.btnLogin);
        mPreferences = PreferenceManager.getDefaultSharedPreferences(this);
        mEditor = mPreferences.edit();

        checkSharedPreferences();

        Login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final String Username = mUsername.getText().toString();
                final String Password = mPassword.getText().toString();
            if (Username.length()==0) {
                mUsername.requestFocus();
                mUsername.setError("Field cannot be empty");
            }
            else if (Username.length()==1) {
                mUsername.requestFocus();
                mUsername.setError("Must be atleast 2 characters");
            }
            else  if(!Username.matches("[a-zA-Z0-9]+")) {
                mUsername.requestFocus();
                mUsername.setError("Field cannot use special characters");
            }
            else if (Password.length()==0) {
                mPassword.requestFocus();
                mPassword.setError("Field cannot be empty");
            }
            else {
                //Save data when remember me checkbox is checked
                if (mCheckbox.isChecked()){
                    mEditor.putString(getString(R.string.CheckboxSave), "True" );
                    mEditor.commit();

                    String UsernameSave = mUsername.getText().toString();
                    mEditor.putString(getString(R.string.UsernameSave),UsernameSave);
                    mEditor.commit();

                    String PasswordSave = mPassword.getText().toString();
                    mEditor.putString(getString(R.string.PasswordSave), PasswordSave);
                    mEditor.commit();
                }
                //Dont save data when remember me checkbox is not checked
                else {
                    mEditor.putString(getString(R.string.CheckboxSave), "False" );
                    mEditor.commit();

                    mEditor.putString(getString(R.string.UsernameSave), "");
                    mEditor.commit();

                    mEditor.putString(getString(R.string.PasswordSave), "");
                    mEditor.commit();
                }
                //Display toast and call method to switch activity
                Toast.makeText(LoginPage.this,"Authentication Successful",Toast.LENGTH_LONG).show();
                New();
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

    public void New() {
        Intent homepage = new Intent(this,MainActivity.class);
        startActivity(homepage);
    }
    public void btnClick (View view) {
        Intent signup = new Intent(this,SignUpPage.class);
        startActivity(signup);
    }

}
