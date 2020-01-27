import React from 'react';
import '../styles/Logout.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

class Logout extends React.Component {
    render() {
        return (
            <div>
                <Container fluid>
                    <Row>
                        <Col xs={{ order:0 }}>
                            <p> Logout Lorem Ipsum </p>
                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }
}

export default Logout;