import React from 'react';
import '../../styles/Healer.css';
import {HEALER_HEAL_PATH, HEALER_PATH} from "../../constants/routes";
import {Image} from "react-bootstrap";
import Jumbotron from "react-bootstrap/Jumbotron";
import ProgressBar from "react-bootstrap/ProgressBar";
import Badge from "react-bootstrap/Badge";
import Button from "react-bootstrap/Button";
import Spinner from "react-bootstrap/Spinner";

class Healer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            buttonState: true,
            isLoading: true,
            npcName: '',
            npcImagePath: '',
            npcText: '',
            charGold: 0,
            price: 0,
            health: 0,
            maxHealth: 0,
            progressBarVariant: '',
            healingStatus: '',
        }
    }

    componentDidMount() {
        this.props.sendGetRequest(HEALER_PATH)
            .then((response) => {
                const health = response['data']['health'];
                const maxHealth = response['data']['max_health'];
                const progressBarVariant = health > (maxHealth / 2) ? 'success' : 'warning';
                const buttonState = health !== maxHealth;
                this.setState({npcName: response['data']['name']});
                this.setState({npcImagePath: response['data']['img_path']});
                this.setState({npcText: response['data']['text']});
                this.setState({charGold: response['data']['gold']});
                this.props.setCharacterGold(response['data']['gold']);
                this.setState({price: response['data']['price']});
                this.setState({health: health});
                this.setState({maxHealth: maxHealth});
                this.setState({progressBarVariant: progressBarVariant});
                this.setState({buttonState: buttonState});
                this.setState({isLoading: false});
            }).catch((error) => {
                this.setState({healingStatus: error.response['data']['message']});
        })
    }

    healerHeal = () => {
        this.props.sendPostRequest(HEALER_HEAL_PATH, {})
            .then((response) => {
                const paid = response['data']['paid'];
                const newPrice = this.state.price - paid;
                const healingStatus = 'You were healed for ' + response['data']['healed_for'] +
                    ' and paid ' + paid + ' gold.';
                this.setState({health: response['data']['health']});
                this.setState({charGold: response['data']['gold']});
                this.props.setCharacterGold(response['data']['gold']);
                this.setState({price: newPrice});
                this.setState({buttonState: false});
                this.setState({progressBarVariant: 'success'});
                this.setState({healingStatus: healingStatus});
            }).catch((error) => {
                console.log(error.response);
                this.setState({healingStatus: error.response['data']['message']});
        });
    };

    render() {
        if (!this.state.isLoading) {
            return (
                <Jumbotron>
                    <div className="text-center">
                        <Image
                            src={this.state.npcImagePath}
                            height={400}
                            width={280}
                            alt="healer image"
                        />
                        <span className="mt-3 align-text-bottom form-control">
                            <strong>{this.state.npcName}</strong>: {this.state.npcText}
                        </span>
                        <
                            ProgressBar
                            className="bg-danger mb-0 mt-1"
                            variant={this.state.progressBarVariant}
                            now={this.state.health}
                            max={this.state.maxHealth}
                        />
                        <p>
                            <Badge className="text-center mt-0" variant={this.state.progressBarVariant}>
                                {this.state.health} / {this.state.maxHealth}
                            </Badge>
                        </p>
                        <Button
                            size="lg"
                            active={this.state.buttonState}
                            disabled={!this.state.buttonState}
                            onClick={() => this.healerHeal}
                        >
                            Heal for {this.state.price} gold
                        </Button>
                        <p className="mt-1">
                            {this.state.healingStatus}
                        </p>
                    </div>
                </Jumbotron>
            );
        } else {
            return <Spinner animation="primary" />
        }

}
}

export default Healer;