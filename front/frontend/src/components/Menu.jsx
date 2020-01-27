import React from 'react';
import '../styles/Menu.css';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from "react-bootstrap/NavDropdown";
import { NavLink } from 'react-router-dom';
import Button from "react-bootstrap/Button";
import {LOGOUT_PATH, LOGOUT_REFRESH_PATH} from "../constants/routes";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";


class Menu extends React.Component {
    handleLogout = () => {
        this.props.sendPostRequest(LOGOUT_PATH, {})
            .then((response) => {
                this.props.setIsAuthenticated(false);
            }).catch((error) => {
                console.log(error.response);
        });
        this.props.sendPostRequest(LOGOUT_REFRESH_PATH, {}, true)
            .then((response) => {
            }).catch((error) => {
                console.log(error.response);
        });
    };

    render() {
        return (
            <div className={this.props.className}>
                <Navbar  collapseOnSelect expand="lg" bg="dark" variant="dark">
                    <Navbar.Brand href={"/character"}>Garden and Graves</Navbar.Brand>
                    <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                    <Navbar.Collapse id="responsive-navbar-nav">
                        <Nav fill className="ml-auto" variant="pills">
                            <Nav.Link as={NavLink} to="/character">Character</Nav.Link>
                            <NavDropdown title="Fights" id="collasible-nav-dropdown">
                                <NavDropdown.Item as={NavLink} to="/arena">Arena</NavDropdown.Item>
                                <NavDropdown.Item as={NavLink} to="/expedition">Expedition</NavDropdown.Item>
                            </NavDropdown>
                            <NavDropdown title="NPC" id="collasible-nav-dropdown">
                                <NavDropdown.Item as={NavLink} to="/npc/healer">Healer</NavDropdown.Item>
                                <NavDropdown.Item as={NavLink} to="/npc/trader">Trader</NavDropdown.Item>
                            </NavDropdown>

                            <Nav.Link as={NavLink} to={"/ranking"}>Ranking</Nav.Link>
                            <Nav.Link as={NavLink} to={"/manage"}>Account Management</Nav.Link>
                            <Button variant="dark" onClick={this.handleLogout}>
                                Logout
                            </Button>
                        </Nav>
                    </Navbar.Collapse>
                </Navbar>
                <Row className="pt-0 mt-0 w-25 mr-auto ml-auto mb-2 text-center" style={{backgroundColor: "#D4CECD"}}>
                    <Col>
                        Level: {this.props.characterLevel}
                    </Col>
                    <Col>
                        Gold: {this.props.characterGold}
                    </Col>
                </Row>
            </div>
        );
    }
}

export default Menu;