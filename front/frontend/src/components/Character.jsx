import React from 'react';
import '../styles/Character.css';
import Jumbotron from "react-bootstrap/Jumbotron";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import {
    CHARACTER_PATH, CHARACTER_STAT_DISPLAY_NAME,
} from "../constants/routes";
import Spinner from "react-bootstrap/Spinner";
import CharacterEquipment from "./SubComponents/CharacterEquipment";
import CharacterStats from "./SubComponents/CharacterStats";

class Character extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            characterData: {},
            isLoading: true,
            freeStats: 0,
            }
        }

    componentDidMount() {
    this.props.sendGetRequest(CHARACTER_PATH)
            .then((response) => {
                this.setState({characterData: response['data']});
                this.setState({freeStats: response['data']['free_stats']});
                this.props.setCharacterGold(response['data']['gold']);
                this.props.setCharacterLevel(response['data']['level']);
                this.setState({isLoading: false});
            }).catch((error) => {
                console.log(error.response);
        });
    };

    setFreeStats = (newFreeStats) => {
        this.setState({freeStats: newFreeStats});
    };

    setCharacterData = (newCharacterData) => {
        this.setState({characterData: newCharacterData});
    };

    render() {
        if (!this.state.isLoading) {
            return (
                <Jumbotron className="character-view">
                    <Container>
                        <Row className="justify-content-md-center">
                            <Col md="auto">
                                <h3>{this.state.characterData['name']}</h3>
                            </Col>
                        </Row>

                        <CharacterEquipment
                            characterData={this.state.characterData}
                        />
                        <Row className="justify-content-center">
                            <Col md={"auto"}>
                                <CharacterStats
                                    toRender={CHARACTER_STAT_DISPLAY_NAME}
                                    characterData={this.state.characterData}
                                    sendPostRequest={this.props.sendPostRequest}
                                    manageStats={true}
                                    setFreeStates={this.setFreeStats}
                                    setCharacterData={this.setCharacterData}
                                    freeStats={this.state.freeStats}
                                />
                            </Col>
                        </Row>
                    </Container>
                </Jumbotron>
            );
        }
        else {
            return (
                <Spinner animation="primary" />
            )
        }
    }
}

export default Character;