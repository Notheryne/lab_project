import React from 'react';
import '../styles/Expedition.css';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import {ENEMY_STAT_DISPLAY_NAME, EXPEDITION_FIGHT_PATH, EXPEDITION_PATH} from "../constants/routes";
import Spinner from "react-bootstrap/Spinner";
import {Image} from "react-bootstrap";
import CharacterStats from "./SubComponents/CharacterStats";
import Button from "react-bootstrap/Button";
import FightResult from "./SubComponents/FightResult";
import Jumbotron from "react-bootstrap/Jumbotron";

class Expedition extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            enemyData: {},
            fightData: {},
            buttonActive: true,
            showResult: false,
            isLoading: true,
            status: '',
        }
    }

    componentDidMount() {
        this.props.sendGetRequest(EXPEDITION_PATH)
            .then((response) => {
                this.setState({enemyData: response['data']['enemy']});
                this.props.setCharacterGold(response['data']['gold']);
                this.props.setCharacterLevel(response['data']['level']);
                this.setState({isLoading: false});
            }).catch((error) => {
                console.log(error.response);
        })
    }

    performMonsterFight = () => {
        this.props.sendPostRequest(EXPEDITION_FIGHT_PATH, {defender_id: this.state.enemyData['id']})
            .then((response) => {
                this.setState({fightData: response['data']});
                this.setState({showResult: true});
                this.props.setCharacterGold(response['data']['gold']);
                this.props.setCharacterLevel(response['data']['level']);
                this.setState({buttonActive: false});
            }).catch((error) => {
            this.setState({status: error.response['data']['message']});
        });
    };

    render() {
        if (!this.state.isLoading) {
            return (
                <Jumbotron>
                    <Row className="justify-content-center">
                          <Image
                                src={this.state.enemyData['image_path']}
                                alt="monster image"
                                height={350}
                                width={250}
                            />
                    </Row>
                    <Row className="justify-content-center">
                        <h3>{this.state.enemyData['name']}</h3>
                    </Row>
                    <Row className="justify-content-center">
                        <CharacterStats
                            toRender={ENEMY_STAT_DISPLAY_NAME}
                            characterData={this.state.enemyData}
                            sendPostRequest={this.props.sendPostRequest}
                            manageStats={false}
                        />
                    </Row>
                    <Row className="justify-content-center">
                        <Col md={{span: 3}}>
                            <Button
                                block
                                className=""
                                size="lg"
                                variant="warning"
                                onClick={this.performMonsterFight}
                                active={this.state.buttonActive}
                                disabled={!this.state.buttonActive}
                            >
                                Attack
                            </Button>
                        </Col>
                    </Row>
                     <Row className="justify-content-center">
                         <p>{this.state.status}</p>
                     </Row>
                    <FightResult
                        show={this.state.showResult}
                        fightCourse={this.state.fightData}
                    />
                </Jumbotron>

            );
        } else {
            return <Spinner animation="primary"/>
        }
    }
}

export default Expedition;