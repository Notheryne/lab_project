import React, {Component} from 'react';
import axios from 'axios';

import { REGISTER_PATH } from "../../constants/routes";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Jumbotron from "react-bootstrap/Jumbotron";
import Image from "react-bootstrap/Image";
import logo from "../../assets/logo.svg";
import "../../styles/Register.css";

class Register extends Component {
    constructor(props) {
        super(props);
        this.state = {
            serverMessage: '',
        }

    }

    handleRegister = (event) => {
        event.preventDefault();
        let username = event.target.username.value;
        let email = event.target.email.value;
        let password = event.target.password.value;
        let characterName = event.target.charactername.value;
        axios.post(REGISTER_PATH, {
            username: username,
            password: password,
            email: email,
            char_name: characterName,
        }).then((response) => {
            const data = response['data'];
            window.localStorage.setItem('access_token', data['access_token']);
            window.localStorage.setItem('refresh_token', data['refresh_token']);
            this.setState({serverMessage: data['message']});
            this.props.setIsAuthenticated(true);
        })
            .catch((error) => {
                console.log(error.response);
                this.props.setIsAuthenticated(false);
                this.setState({serverMessage: error.response['data']['message']})
            })
    };

    render() {
        return (
            <Jumbotron className="not-authorized-jumbotron">
                <Image roundedCircle src={logo} alt="Game logo image" className="logo-image" />
                <div className="initial-form">
                    <Form onSubmit={this.handleRegister}>
                        <Form.Group controlId="username">
                            <Form.Label size="lg">Username</Form.Label>
                            <Form.Control name="username" type="username" placeholder="Enter username" size="lg" />
                        </Form.Group>
                        <Form.Group controlId="email">
                            <Form.Label size="lg">Email</Form.Label>
                            <Form.Control name="email" type="username" placeholder="Enter email" size="lg" />
                        </Form.Group>
                        <Form.Group controlId="characterName">
                            <Form.Label size="lg">Character Name</Form.Label>
                            <Form.Control name="charactername" type="username" placeholder="Enter character name" size="lg" />
                        </Form.Group>
                        <Form.Group controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control name="password" type="password" placeholder="Password" size="lg" />
                        </Form.Group>
                        <Form.Text className="text-muted server-message">{this.state.serverMessage}</Form.Text>
                        <Button variant="primary" type="submit" size="lg" block>
                            Sign Up
                        </Button>
                    </Form>
                </div>
            </Jumbotron>
        );
    }
}

export default Register;