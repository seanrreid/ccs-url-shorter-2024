/* eslint-disable react/prop-types */
import styled from 'styled-components';

const List = styled.ul`
    display: flex;
    flex-wrap: wrap;
    list-style: none;
    margin: 0;
    max-width: 40rem;
    margin: 1rem auto;
    padding: 0;

    li {
        display: flex;
        padding: 8px 0;
        width: 100%;
    }
`;

export default function LinkList({ linkList }) {
    // const src_url = import.meta.env.VITE_SOURCE_URL;
    const src_url = 'http://localhost:8000'
    return (
        <List>
            {linkList.map((link, id) => {
                return (
                    <li key={id}>
                        <a
                            href={`${src_url}/sendit?url=${link.short_url}`}
                            title={`Short link to ${link.title}`}
                            target='_blank'
                            rel='noreferrer'
                        >
                            {link.title}
                        </a>
                    </li>
                );
            })}
        </List>
    );
}
