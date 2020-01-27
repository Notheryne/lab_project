import React, {Component} from 'react';
import axios from 'axios';

import { LOGIN_PATH } from "../../constants/routes";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Jumbotron from "react-bootstrap/Jumbotron";
import Image from "react-bootstrap/Image";
import logo from "../../assets/logo.svg";
import "../../styles/Login.css";

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            serverMessage: '',
        }

    }

    handleLogin = (event) => {
        event.preventDefault();
        let username = event.target.username.value;
        let password = event.target.password.value;
        axios.post(LOGIN_PATH, {
            username: username,
            password: password,
        }).then((response) => {
            const data = response['data'];
            window.localStorage.setItem('access_token', data['access_token']);
            window.localStorage.setItem('refresh_token', data['refresh_token']);
            this.setState({serverMessage: data['message']});
            this.props.setIsAuthenticated(true);
        })
            .catch((error) => {
                this.props.setIsAuthenticated(false);
                this.setState({serverMessage: error.response['data']['message']})
            })
    };

    render() {
        return (
            <Jumbotron className="not-authorized-jumbotron">
                <Image roundedCircle src={logo} alt="Game logo image" className="logo-image" />
                <div className="initial-form">
                    <Form onSubmit={this.handleLogin}>
                        <Form.Group controlId="formBasicEmail">
                            <Form.Label size="lg">Username</Form.Label>
                            <Form.Control name="username" type="username" placeholder="Enter username" size="lg" />
                        </Form.Group>
                        <Form.Group controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control name="password" type="password" placeholder="Password" size="lg" />
                        </Form.Group>
                        <Form.Text className="text-muted server-message">{this.state.serverMessage}</Form.Text>
                        <Button variant="primary" type="submit" size="lg" block>
                            Log me In
                        </Button>
                        <Button variant="primary" href={'/register'} size="lg" block>
                            Sign Up
                        </Button>
                    </Form>
                </div>
            </Jumbotron>
        );
    }
}

export default Login;