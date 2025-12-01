import Link from "next/link";

export default function Page(){
    return (
    <div>
        <h1>What do you wish to do?</h1>
        <h2>
            <Link href="users/admin">Admin Login</Link>
        </h2>
        <h2>
            <Link href="users/login">User Login</Link>
        </h2>
        <h2>
            <Link href="users/signup">Register New User</Link>
        </h2>
        <h2>
            <Link href="users/logout">Logout</Link>
        </h2>
    </div>
);
}