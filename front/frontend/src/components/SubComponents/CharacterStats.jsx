import React, {Component} from 'react';
import Col from "react-bootstrap/Col";
import {ADD_STATS_PATH, INCREASING_STATS} from "../../constants/routes";
import Button from "react-bootstrap/Button";
import '../../styles/CharacterStats.css';

class CharacterStats extends Component {
    renderCharacterStats = () => {
        let char = this.props.characterData;
        const stats = Object.keys(this.props.toRender).map(statName => {
            const renderButton = INCREASING_STATS[statName];
            return (
                <li key={statName}>
                    <strong>{this.props.toRender[statName]}</strong>: {char[statName]}
                    {(renderButton && this.props.manageStats)
                        ? <Button
                            className="stats-button btn-circle"
                            variant="primary"
                            size="sm"
                            active={this.props.freeStats !== 0}
                            disabled={this.props.freeStats === 0}
                            onClick={() => {
                                this.props.sendPostRequest(ADD_STATS_PATH, {'stat': statName})
                                    .then((response) => {
                                        char[response['data']['increased']] += response['data']['increased_by'];
                                        this.props.setCharacterData(char);
                                        this.props.setFreeStates(this.props.freeStats - 1);
                                        this.setState({characterData: char});
                                    });
                            }}
                        >+</Button>
                        : null
                    }
                </li>
            )
        });
        return (
            <ul className="list-unstyled text-center">
                {stats}
            </ul>
        )
    };

    render() {
        return (
            <Col className="stats-viewer">
                {this.renderCharacterStats()}
            </Col>
        );
    }
}

export default CharacterStats;