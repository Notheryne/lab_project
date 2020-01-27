import React from 'react';
import '../styles/Manage.css';
import {MANAGE_PATH, MANAGE_STAT_PATH} from "../constants/routes";
import Jumbotron from "react-bootstrap/Jumbotron";
import Row from "react-bootstrap/Row";
import Alert from "react-bootstrap/Alert";
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import Spinner from "react-bootstrap/Spinner";
import Modal from "react-bootstrap/Modal";

class Manage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: true,
            accountData: {},
            changeStatus: '',
            email: '',
            showConfirmationWindow: false,
        }
    };

    componentDidMount() {
        this.props.sendGetRequest(MANAGE_PATH)
            .then((response) => {
                this.setState({accountData: response['data']});
                this.setState({isLoading: false});
            }).catch((error) => {
                console.log(error.response);
        })
    }

    pushChange = (event, statName) => {
        event.preventDefault();
        const newStat = event.target[statName].value;
        this.props.sendPostRequest(MANAGE_STAT_PATH,
            {stat_name: statName, value: newStat})
            .then((response) => {
                this.setState({changeStatus: response.data.message});
            }).catch((error) => {
                if (error.response.data.message.value) {
                    this.setState({changeStatus: error.response.data.message.value})
                } else {
                    this.setState({changeStatus: error.response.data.message});
                }
        })
    };

    changeableStatRender = (statName, className) => {
        const statNameToBeRendered = statName.replace('_', ' ');
        return (
            <Accordion defaultActiveKey="0" className={className} key={"changeable-" + statName}>
                <Card>
                    <Accordion.Toggle as={Card.Header} eventKey="0">
                        <h5 className="text-capitalize d-inline">{statNameToBeRendered}: </h5>
                        <h5 className="d-inline">{this.state.accountData[statName]['value']}</h5>
                        <h6 className="d-inline float-right no-select">&#9660;</h6>
                    </Accordion.Toggle>
                    <Accordion.Collapse eventKey="0">
                        <Card.Body>
                            <Form onSubmit={(event) => this.pushChange(event, statName)}>
                                <Form.Group
                                    as={Row}
                                    controlId={"form-" + statNameToBeRendered + "-change"}
                                    className="mb-0"
                                >
                                    <Form.Label column className="text-capitalize">
                                        New {statNameToBeRendered}
                                    </Form.Label>
                                    <Col md={{span: 7}}>
                                        <Form.Control type="username" name={statName} placeholder={statNameToBeRendered} />
                                    </Col>
                                    <Col md={{span: 2}}>
                                        <Button block type="submit">
                                            Change
                                        </Button>
                                    </Col>
                                </Form.Group>
                            </Form>
                        </Card.Body>
                    </Accordion.Collapse>
                </Card>
            </Accordion>
        )
    };

    renderChangeableStats = (className) => {
        return Object.keys(this.state.accountData).map((statName) => {
            if (this.state.accountData[statName]['changeable']) {
                return this.changeableStatRender(statName, className);
            } else {
                return null;
            }
        });
    };

    handleShowConfirmationWindow = () => {this.setState({showConfirmationWindow: true})};
    handleHideConfirmationWindow = () => {this.setState({showConfirmationWindow: false})};

    deleteAccount = () => {
        this.props.sendDeleteRequest(MANAGE_STAT_PATH)
            .then((response) => {
                window.localStorage.setItem("access_token", null);
                window.localStorage.setItem("refresh_token", null);
                this.props.setIsAuthenticated(false);
            }).catch((error) => {
                console.log(error.response);
        })
    };

    showConfirmationWindow = () => {
        return (
            <Modal
                show={this.state.showConfirmationWindow}
                onHide={this.handleHideConfirmationWindow}
            >
                <Modal.Header closeButton>
                    <Modal.Title>Confirm account deletion</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    <p>Dear <strong>{this.state.accountData['username']['value']}</strong>, are you sure that
                        you want to remove your account? </p>
                    <p>If you proceed with this, retrieving your account or your progress will not
                        be possible.</p>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="danger" onClick={() => this.deleteAccount()}>
                        Confirm
                    </Button>
                    <Button variant="primary" onClick={this.handleHideConfirmationWindow}>
                        Cancel
                    </Button>
                </Modal.Footer>
            </Modal>
        )
    };

    render() {
        const rowClassNameControl = "ml-auto mr-auto mt-2 mb-2 w-75";
        if (!this.state.isLoading) {
            return (
                <Jumbotron className="text-center">
                    <Alert variant="dark" className={rowClassNameControl}>
                        <h2>Username: {this.state.accountData['username']['value']}</h2>
                    </Alert>
                        <Alert variant="dark" className={rowClassNameControl}>
                            <h4>Account created on {
                                this.state.accountData['create_day']['value'] + ' (' +
                                this.state.accountData['create_hour']['value'] + ')'
                            }
                            </h4>
                    </Alert>
                    {this.renderChangeableStats(rowClassNameControl)}
                    <Button
                        variant="danger"
                        onClick={() => this.handleShowConfirmationWindow()}
                    >
                        Delete your account
                    </Button>
                    {this.showConfirmationWindow()}
                    <p className="pb-0 mb-0 ml-auto mt-auto">{this.state.changeStatus}</p>
                </Jumbotron>
            );
        } else {
            return (
                <Spinner animation="primary" />
            )
        }
    }
}

export default Manage;