import React, {Component} from 'react';
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import { NavLink} from "react-router-dom";

import '../../styles/NotLoggedInMenu.css';

class NotLoggedInMenu extends Component {
    render() {
        return (
            <div className="top-side-menu">
                <Navbar collapseOnSelect className={this.props.className} expand="lg" bg="dark" variant="dark">
                    <Nav fill className={"mr-auto"}>
                        <Nav.Link href="https://github.com/Notheryne/lab_project" target="_blank">
                            Source Code
                        </Nav.Link>
                    </Nav>
                    <Nav fill className={"ml-auto"}>
                        <Nav.Link as={NavLink} to={'/ranking'}>
                            Ranking
                        </Nav.Link>

                        <Nav.Link as={NavLink} to={'/login'}>
                            Log In
                        </Nav.Link>

                        <Nav.Link as={NavLink} to={'/register'}>
                            Sign Up
                        </Nav.Link>
                    </Nav>
                </Navbar>
            </div>

        );
    }
}

export default NotLoggedInMenu;