import React, {Component} from 'react';
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import "../../styles/FightResult.css";

class FightResult extends Component {
    constructor(props) {
        super(props);
        this.state = {
            roundsReady: false,
        }
    }


    renderRounds = () => {
        const roundsDescription = this.props.fightCourse['rounds'];
        const rounds = roundsDescription.map((roundData, roundNumber) => {
            const round = 'Round #' + (roundNumber + 1);
            let attackerMisc;
            let defenderMisc;

            if (roundData['attacker_critical'] && roundData['defender_dodge']) {
                attackerMisc = ' (critical, dodged).';
            } else if (roundData['attacker_critical']) {
                attackerMisc = ' (critical).';
            } else if (roundData['defender_dodge']) {
                attackerMisc = ' (dodged).';
            } else {
                attackerMisc = '.';
            }

            if (roundData['defender_critical'] && roundData['attacker_dodge']) {
                defenderMisc = ' (critical, dodged).';
            } else if (roundData['defender_critical']) {
                defenderMisc = ' (critical).';
            } else if (roundData['attacker_dodge']) {
                defenderMisc = ' (dodged).';
            } else {
                defenderMisc = '.';
            }

            return (
                <React.Fragment key={'fragment' + roundNumber}>
                    <h3 key={round} className="text-center">{round}</h3>
                        <p className="ml-6 mb-0 text-center" key={'attacker' + roundNumber}>
                            Attacker attacks. The attack has done {roundData['attacker_damage']} damage
                            {attackerMisc} Defender has {roundData['defender_health']} health left.
                        </p>
                        <p className="mr-6 mt-0 text-center" key={'defender'  + roundNumber}>
                            Defender's turn. His attack has done {roundData['defender_damage']} damage
                            {defenderMisc} Attacker has {roundData['attacker_health']} health left.
                        </p>
                </React.Fragment>
            );
        });
        return (
            <ol key={"rounds-list"} className="list-group-item-light list-unstyled">
                {rounds}
            </ol>
        )
    };

    render() {
        if (this.props.show) {
            return (
                <React.Fragment>
                    <Accordion defaultActiveKey="1" className="fight-result-accordion">
                        <Card>
                            <Accordion.Toggle as={Card.Header} eventKey="0">
                                Winner:
                                <strong>
                                    {
                                        this.props.fightCourse['winner']
                                        ? " You!"
                                        : " Not you"
                                    }
                                </strong>
                            </Accordion.Toggle>
                            <Accordion.Collapse eventKey="0">
                                <Card.Body>
                                    {this.renderRounds()}
                                </Card.Body>
                            </Accordion.Collapse>
                        </Card>
                    </Accordion>
                </React.Fragment>
            );
        }
        return <p></p>
    }
}

export default FightResult;