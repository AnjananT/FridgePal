import './Steps.css'

function Steps(props) {
    return (
        <div className = 'steps-container'>
            <h2 className = 'step-number'> {props.stepNumber} </h2>
            <h2> {props.stepText}</h2>
        </div>
    )
}

export default Steps