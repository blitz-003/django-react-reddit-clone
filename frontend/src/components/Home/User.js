import PropTypes from "prop-types";

const User = (props) => {
    return (
        <span className="username">
            Posted by {props.username}
        </span>
    )
}

User.propTypes = {
    username: PropTypes.string
}

export default User
