package com.example.paloslanesapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.telecom.Call;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;


public class SignUpPage extends AppCompatActivity {

    EditText bDay;
    EditText fname;
    EditText lname;
    EditText email;
    EditText phone;
    EditText newUser;
    EditText newPass;
    EditText confirm;
    Button submit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up_page);

        //Create references to UI
        final EditText fname = (EditText) findViewById(R.id.editFname);
        final EditText lname = (EditText) findViewById(R.id.editLname);
        final EditText email = (EditText) findViewById(R.id.editEmail);
        final EditText phone = (EditText) findViewById(R.id.editPhone);
        final EditText bDay = (EditText) findViewById(R.id.editBirthDate);
        Button submit = (Button) findViewById(R.id.btnSubmit);

        //Format text for dates with /
        bDay.addTextChangedListener(new TextWatcher() {

            int beforeLength;

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                beforeLength = bDay.length();
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int count, int after) {
                int dates = bDay.getText().toString().length();
                if (beforeLength < dates && (dates == 2 || dates == 5)) {
                    bDay.append("/");
                }
            }

            @Override
            public void afterTextChanged(Editable s) {}
        });

        //Format text for phone numbers with -
        phone.addTextChangedListener(new TextWatcher() {

            int beforeLength;

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                beforeLength = phone.length();
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                int digits = phone.getText().toString().length();
                if (beforeLength < digits && (digits == 3 || digits == 7)) {
                    phone.append("-");
                }
            }

            @Override
            public void afterTextChanged(Editable s) { }
        });

        //Create onClickListener for button submit
        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            //Validate text when submit button is clicked
            public void onClick(View view) {
                final String FirstName = fname.getText().toString();
                final String LastName = lname.getText().toString();
                final String Email = email.getText().toString();
                final String Phone = phone.getText().toString();
                final String Birthday = bDay.getText().toString();
                //validate first name text
                if (FirstName.length()==0) {
                    fname.requestFocus();
                    fname.setError("Field cannot be empty");
                }
                else if (FirstName.length()==1) {
                    fname.requestFocus();
                    fname.setError("Must be atleast 2 characters");
                }
                else if (!FirstName.matches("[a-zA-Z]+")) {
                    fname.requestFocus();
                    fname.setError("Use only alphabetical characters");
                }
                //validate last name text
                else if (LastName.length()==0) {
                    lname.requestFocus();
                    lname.setError("Field cannot be empty");
                }
                else if (LastName.length()==1) {
                    lname.requestFocus();
                    lname.setError("Must be atleast 2 characters");
                }
                else if (!LastName.matches("[a-zA-Z]+")) {
                    lname.requestFocus();
                    lname.setError("Use only alphabetical characters");
                }
                //Validate birthday text
                else if (Birthday.length()!=10) {
                    bDay.requestFocus();
                    bDay.setError("Must us the format 00/00/0000");
                }
                else if (!Birthday.matches("[0-9/]+")) {
                    bDay.requestFocus();
                    bDay.setError("Use only numerical characters");
                }
                //Validate email text
                else if (Email.length()==0) {
                    email.requestFocus();
                    email.setError("Field cannot be empty");
                }
                //Validate phone text
                else if (Phone.length()!=12) {
                    phone.requestFocus();
                    phone.setError("Must use format 123-123-1234");
                }
                else if (!Phone.matches("[0-9-]+")) {
                    phone.requestFocus();
                    phone.setError("Use only numerical values");
                }
                else {
                    Toast.makeText(SignUpPage.this,"Thank you for signing up",Toast.LENGTH_LONG).show();
                    New();
                }
            }
        });
    }
    public void New() {
        Intent homepage = new Intent(this,MainActivity.class);
        startActivity(homepage);
    }

}
