import { useState, useEffect } from 'react';
import axios from 'axios'; // axiosをインポート
import './App.css'
// バックエンドAPIのURL (環境変数にするのが望ましいですが、まずはハードコードで)
// const API_URL = 'http://127.0.0.1:5000/bookmarks';
const API_URL = import.meta.env.VITE_API_BASE_URL + '/bookmarks';

function App() {
  const [bookmarks, setBookmarks] = useState([]); // ブックマーク一覧を保持するstate
  const [url, setUrl] = useState(''); // フォームのURL入力値を保持するstate
  const [title, setTitle] = useState(''); // フォームのタイトル入力値を保持するstate
  const [description, setDescription] = useState(''); // フォームの説明入力値を保持するstate

  // --- 1. 一覧取得機能 ---
  // コンポーネントが最初に表示されたときにブックマーク一覧を取得する
  useEffect(() => {
    fetchBookmarks();
  }, []);

  const fetchBookmarks = async () => {
    try {
      const response = await axios.get(API_URL);
      setBookmarks(response.data);
    } catch (error) {
      console.error('Error fetching bookmarks:', error);
    }
  };

  // --- 2. 新規登録機能 ---
  const handleFormSubmit = async (e) => {
    e.preventDefault(); // フォームのデフォルトの送信動作を防ぐ

    if (!url) {
      alert('URLは必須です');
      return;
    }

    try {
      // バックエンドAPIにPOSTリクエストを送信
      const response = await axios.post(API_URL, {
        url: url,
        title: title,
        description: description,
      });
      
      // 登録成功後、一覧を再取得して画面を更新
      fetchBookmarks();
      
      // フォームをリセット
      setUrl('');
      setTitle('');
      setDescription('');
      
    } catch (error) {
      console.error('Error creating bookmark:', error);
    }
  };

  // --- 3. 表示部分 (JSX) ---
  return (
    <div>
      <h1>ブックマーク一覧</h1>

      {/* 新規登録フォーム */}
      <form onSubmit={handleFormSubmit}>
        <h2>新規ブックマーク追加</h2>
        <div>
          <label>URL: </label>
          <input type="text" value={url} onChange={(e) => setUrl(e.target.value)} required />
        </div>
        <div>
          <label>タイトル: </label>
          <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
        </div>
        <div>
          <label>説明: </label>
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} />
        </div>
        <button type="submit">追加</button>
      </form>

      {/* ブックマーク一覧 */}
      <h2>ブックマーク一覧</h2>
      <ul>
        {bookmarks.map((bookmark) => (
          <li key={bookmark.id}>
            <h3><a href={bookmark.url} target="_blank" rel="noopener noreferrer">{bookmark.title || bookmark.url}</a></h3>
            <p>{bookmark.description}</p>
            <p><small>Created at: {new Date(bookmark.created_at).toLocaleString()}</small></p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;