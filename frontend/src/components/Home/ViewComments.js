import PropTypes from "prop-types";
import { useState, useEffect } from "react";
import { BiCommentDetail } from "react-icons/bi";

const ViewComments = (props) => {

    const [numComments, setNumComments] = useState();
    
    async function getNumberOfComments() {
        const response = await fetch(`http://localhost:8000/api/post/num-comments/id=${props.postId}/`);
        if (response.ok) {
            const json = await response.json();
            console.log(json);
            setNumComments(json.num_comments);
        } else {
            throw new Error ("Couldn't get number of comments!");
        }
    }

    useEffect(() => {
        getNumberOfComments();
    }, []);

    return ( 
        <div className="nav-to-comments" onClick={() => props.navigateToPost(props.postId)}>
            <BiCommentDetail />
            <span>{numComments} {numComments === 1 ? "Comment" : "Comments"}</span>
        </div>
    );
}

ViewComments.propTypes = {
    postId: PropTypes.string,
    navigateToPost: PropTypes.func
}

export default ViewComments;
