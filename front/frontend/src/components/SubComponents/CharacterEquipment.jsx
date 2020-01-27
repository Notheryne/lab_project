import React, {Component} from 'react';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import {ITEM_STAT_DISPLAY_NAME, PLACEHOLDER_IMAGES} from "../../constants/routes";
import Tooltip from "react-bootstrap/Tooltip";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Image from "react-bootstrap/Image";
import '../../styles/CharacterEquipment.css';
import Container from "react-bootstrap/Container";


class CharacterEquipment extends Component {
    getItemImagePath = (gameItemType) => {
        return this.props.characterData['items'][gameItemType]['image_path'];
    };

    getItemDescription = (gameItemType) => {
        const item = this.props.characterData['items'][gameItemType];
        const stats = Object.keys(ITEM_STAT_DISPLAY_NAME).map(statName => {
            return (
                <p key={statName} className="item-description-row">{ITEM_STAT_DISPLAY_NAME[statName]}: {item[statName]}</p>
            );
        });
        return (
            <Tooltip id="tooltip-bottom">
                <strong>{item['name']}</strong> <br/>
                <small>{item['slot']}</small> <br/>
                {stats}
            </Tooltip>
        );
    };

    renderImageWithDescription = (gameItemType, gameItemHeight, gameItemWidth) => {
        if (gameItemType in this.props.characterData['items']) {
            return (
                <OverlayTrigger
                    trigger="hover"
                    placement="bottom"
                    overlay={this.getItemDescription(gameItemType)}
                >
                    <Image
                        className="item-image p-2"
                        src={this.getItemImagePath(gameItemType)}
                        height={gameItemHeight}
                        width={gameItemWidth}
                        alt={"character " + gameItemType}
                    />
                </OverlayTrigger>
            )
        } else {
            return (
                <Image
                    className="item-image p-2 item-placeholder-image"
                    src={PLACEHOLDER_IMAGES[gameItemType]}
                    height={gameItemHeight}
                    width={gameItemWidth}
                    alt={"character " + gameItemType}
                />
            )
        }
    };

    render() {
        return (
            <Container className="equipment-background p-2">
                <Row className="justify-content-md-center">
                    <Col xs md="1"> </Col>
                    <Col md={"auto"}>
                        {this.renderImageWithDescription('helmet', 75, 80)}
                    </Col>
                    <Col md="1" className="pt-4">
                        {this.renderImageWithDescription('amulet', 40, 40)}
                    </Col>
                </Row>
                <Row className="justify-content-md-center mt-3">
                    <Col xs lg="2" className="text-right">
                        {this.renderImageWithDescription('weapon', 155, 110)}
                    </Col>
                    <Col md="auto">
                        {this.renderImageWithDescription('armor', 155, 110)}
                    </Col>
                    <Col xs lg="2" className="text-left">
                        {this.renderImageWithDescription('shield', 155, 110)}
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default CharacterEquipment;