import Post from "./Post";
import "../../style/posts.css";
import PropTypes from "prop-types";

const Posts = (props) => {
    
    return (
        <div className="posts">
            {props.posts.map((post) => <Post 
            key={post.id}
            id={post.id}
            username={post.username}
            categoryId={post.category}
            categoryName={post.category_name}
            title={post.title}
            content={post.content}
            numUpvotes={post.num_upvotes}
            numDownvotes={post.num_downvotes}
            dateCreated={post.date_created}
            />)
            }
        </div>
    )
}

Post.propTypes = {
    posts: PropTypes.object
}

export default Posts


