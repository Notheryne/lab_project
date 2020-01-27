import React from 'react';
import '../styles/Arena.css';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import {ARENA_FIGHT_PATH, ARENA_PATH, CHARACTER_STAT_DISPLAY_NAME} from "../constants/routes";
import Spinner from "react-bootstrap/Spinner";
import CharacterEquipment from "./SubComponents/CharacterEquipment";
import CharacterStats from "./SubComponents/CharacterStats";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import FightResult from "./SubComponents/FightResult";
import Jumbotron from "react-bootstrap/Jumbotron";

class Arena extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            enemyData: {},
            fightData: {},
            isLoading: true,
            status: '',
            showResult: false,
            buttonActive: true,
        }
    }

    componentDidMount() {
        this.props.sendGetRequest(ARENA_PATH)
            .then((response) => {
                this.setState({enemyData: response['data']['enemy']});
                this.setState({isLoading: false});
            }).catch((error) => {
                console.log(error.response);
        })
    }

    performArenaFight = () => {
        this.props.sendPostRequest(ARENA_FIGHT_PATH, {defender_id: this.state.enemyData['id']})
            .then((response) => {
                this.setState({fightData: response['data']});
                this.setState({showResult: true});
                this.setState({buttonActive: false});
            }).catch((error) => {
            this.setState({status: error.response['data']['message']});
        });
    };

    render() {
        if (!this.state.isLoading) {
            return (
                <Jumbotron>
                    <Container className="justify-content-center">
                        <CharacterEquipment
                            characterData={this.state.enemyData}
                        />
                    </Container>
                    <Row className="justify-content-center">
                        <Col md="auto">
                            <CharacterStats
                                toRender={CHARACTER_STAT_DISPLAY_NAME}
                                characterData={this.state.enemyData}
                                sendPostRequest={this.props.sendPostRequest}
                                manageStats={false}
                            />
                        </Col>
                    </Row>
                    <Row className="justify-content-center row">
                        <Col md={"auto"}>
                            <Button
                                className="text-center"
                                variant="warning"
                                size="lg"
                                onClick={this.performArenaFight}
                                active={this.state.buttonActive}
                                disabled={!this.state.buttonActive}
                            >
                                Attack
                            </Button>
                        </Col>
                    </Row>
                    <Row className="justify-content-center">
                        <Col md={"auto"}>
                            <p>{this.state.status}</p>
                        </Col>
                    </Row>
                    <FightResult
                        show={this.state.showResult}
                        fightCourse={this.state.fightData}
                    />
                </Jumbotron>
            );
        } else {
            return (
                <Spinner animation="primary" />
            )
        }
    }
}

export default Arena;