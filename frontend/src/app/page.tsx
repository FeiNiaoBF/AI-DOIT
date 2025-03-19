"use client";
import {useEffect, useState, useRef} from "react";

// 消息类型
type MessageType = {
	role: "user" | "server" | "assistant";
	message: string;
};

// 页面组件
export default function Home() {
	// 状态管理
	// 只要是变动的数据，都应该放在状态管理中
	const [messageList, setMessageList] = useState<MessageType[]>([]);
	const [input, setInput] = useState<string>("");
	const [isLoading, setIsLoading] = useState<boolean>(false);
	// 引用
	const messageEndRef = useRef<HTMLDivElement>(null);

	useEffect(() => {
		// 滚动到底部
		// 当messagesList变化时触发
		if (messageEndRef.current) {
			messageEndRef.current?.scrollIntoView({behavior: "smooth"});
		}
	}, [messageList]);

	// 事件处理
	const handleSubmit = async (e: React.FormEvent) => {
		// 阻止浏览器刷新默认行为
		e.preventDefault();
		// 输入为空时，不发送
		if (!input.trim()) return;
		// 发送消息
		const userMessage: MessageType = {
			role: "user",
			message: input,
		}
		// 发送消息
		setMessageList([...messageList, userMessage]);
		// 清空输入框
		setInput("");

		// 发送请求
		try {
			const response = await fetch("http://localhost:5000/api/chat", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				// req: {message: string}
				body: JSON.stringify({message: input}),
			});
			// 解析响应
			const data = await response.json();
			// res: {success: boolean, response: string}
			// 处理响应
			if (data.success) {
				setMessageList([...messageList, {role: "server", message: data.response.message}]);
			} else {
				setMessageList([...messageList, {role: "server", message: "Error message"}]);
			}
		} catch (error) {
			console.error("Error:", error);
			setMessageList([...messageList, {role: "server", message: "Network error"}]);
		} finally {
			setIsLoading(false);
		}
	}

	// 渲染
	return (
		<div>
			<header className="header">
				<h1>
					Redd Chat
				</h1>
			</header>

			<div>
				<div className="message-list">
					{messageList.map((message, index) => (
						<div key={index} className={`message ${message.role}`}>
							{message.message}
						</div>
					))}
					<div ref={messageEndRef}></div>
				</div>
				<form onSubmit={handleSubmit} className="input-form">
					<input
						type="text"
						value={input}
						onChange={(e) => setInput(e.target.value)}
						placeholder="Type a message..."
						className="input"
					/>
					<button type="submit" className="send-button">
						Send
					</button>
				</form>
			</div>
		</div>
	);
}

