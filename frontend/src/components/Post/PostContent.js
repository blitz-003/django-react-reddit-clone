import { useState, useContext, useEffect } from "react";
import { UserContext } from "../../App";
import PropTypes from "prop-types";
import { getNewAccessTokenIfExpired } from "../../utils/auth";

const PostContent = (props) => {

    const [postContent, setPostContent] = useState(props.content);

    /* This is needed for when the user looks at the comments of the post (i.e. we get to the Post component from the 
    PostSelected component). This is because on first render, postContent is undefined while on second render, it 
    is props.content. Thus, we need a useEffect to set the post content to props.content after second render. Note that
    when user views posts by category or posts on home page, this useEffect hook is not needed. */
    useEffect(() => {
        if (props.content) {
            setPostContent(props.content);
        }
    }, [props.content]);

    const { userIdLoggedIn } = useContext(UserContext);

    async function handleEditPostContent(e) {
        e.preventDefault();

        if (props.userId !== userIdLoggedIn) {
            alert("You do not have permission to edit this post as you did not create it!");
            return;
        } 

        const accessToken = localStorage.getItem("accessToken");
        const gotNewAccessToken = getNewAccessTokenIfExpired(accessToken);

        if (gotNewAccessToken) {
            const response = await fetch(`http://localhost:8000/api/post/id=${props.postId}/user-id=${userIdLoggedIn}/`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${accessToken}`
                },
                body: JSON.stringify({content: postContent})
            });
            if (response.ok) {
                props.editPostContent(props.postId, postContent);
            } else {
                throw new Error("Couldn't edit post!");
            }
        }
        else {
            throw new Error("Couldn't fetch new access token!");
        }
    }

    return (
        <>
            {props.currentlyEditing ? 
                <form className="edit-post-content" onSubmit={handleEditPostContent} >
                    <textarea value={postContent} onChange={(e) => setPostContent(e.target.value)} />
                    <input type="submit" value="Edit" />
                </form>
                : 
                <p className="post-content">
                    {props.content}
                </p>
            }
        </>
    )
}

PostContent.propTypes = {
    content: PropTypes.string,
    currentlyEditing: PropTypes.bool,
    postId: PropTypes.string,
    userId: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.number
    ]),
    editPostContent: PropTypes.func
}

export default PostContent
