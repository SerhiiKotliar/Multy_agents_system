# import os
# import json
# import re
# from pathlib import Path
# from typing import List, Dict, Optional, Tuple
# from datetime import datetime, timedelta
# import uuid
#
#
# class TechnicalAgentA:
#     """
#     Агент А - Технічний спеціаліст
#     Спеціалізація: комп'ютерна техніка та мережі
#     """
#
#     def __init__(self, docs_directory: str = "./docs"):
#         self.docs_directory = Path(docs_directory)
#         self.documents = []
#         self.document_metadata = []
#         self.agent_name = "🤖 Агент А (Технічний спеціаліст)"
#
#         # Завантаження документів
#         self.load_documents()
#
#     def load_documents(self):
#         """Завантаження всіх текстових файлів з директорії docs"""
#         print("🔄 Завантаження технічних документів...")
#
#         text_files = list(self.docs_directory.glob("*.txt"))
#
#         for file_path in text_files:
#             try:
#                 content = file_path.read_text(encoding='utf-8')
#                 self.process_document(content, file_path.name)
#             except Exception as e:
#                 print(f"❌ Помилка завантаження {file_path}: {e}")
#
#     def process_document(self, content: str, source: str):
#         """Обробка документів та розділення на секції"""
#         sections = self.split_into_sections(content)
#
#         for i, section in enumerate(sections):
#             if len(section.strip()) > 50:
#                 keywords = self.extract_keywords(section)
#
#                 self.documents.append({
#                     'content': section.strip(),
#                     'keywords': keywords,
#                     'source': source,
#                     'section_id': i + 1,
#                     'word_count': len(section.split())
#                 })
#
#     def split_into_sections(self, content: str) -> List[str]:
#         """Розділяє текст на логічні секції"""
#         sections = re.split(r'\n\s*\n', content)
#         merged_sections = []
#         current_section = ""
#
#         for section in sections:
#             section = section.strip()
#             if len(section) < 300 and len(current_section) < 1500:
#                 current_section += "\n\n" + section if current_section else section
#             else:
#                 if current_section:
#                     merged_sections.append(current_section)
#                 current_section = section
#
#         if current_section:
#             merged_sections.append(current_section)
#
#         return [s for s in merged_sections if s.strip()]
#
#     def extract_keywords(self, text: str) -> List[str]:
#         """Вилучає ключові слова з тексту"""
#         tech_terms = [
#             'IP', 'MAC', 'Wi-Fi', 'USB', 'HDMI', 'DNS', 'DHCP', 'NAT', 'TCP', 'UDP',
#             'HTTP', 'HTTPS', 'SSH', 'FTP', 'VPN', 'LAN', 'WAN', 'MAN', 'WLAN',
#             'роутер', 'комутатор', 'маршрутизатор', 'хаб', 'мост', 'сервер', 'клієнт',
#             'память', 'процесор', 'відеокарта', 'жорсткий диск', 'SSD', 'оперативна память'
#         ]
#
#         found_terms = []
#         for term in tech_terms:
#             if term.lower() in text.lower():
#                 found_terms.append(term)
#
#         capital_words = re.findall(r'\b[A-ZА-Я][a-zа-я]{2,}\b', text)
#         found_terms.extend(capital_words[:5])
#
#         return list(set(found_terms))
#
#     def search_documents(self, query: str, top_k: int = 3) -> List[Dict]:
#         """Пошук найбільш релевантних документів за запитом"""
#         if not self.documents:
#             return []
#
#         query_lower = query.lower()
#         scored_docs = []
#
#         for doc in self.documents:
#             score = 0
#
#             # Пошук у ключових словах
#             for keyword in doc['keywords']:
#                 if keyword.lower() in query_lower:
#                     score += 3
#
#             # Пошук у контенті
#             content_lower = doc['content'].lower()
#             if query_lower in content_lower:
#                 score += 5
#
#             query_words = query_lower.split()
#             word_matches = sum(1 for word in query_words if len(word) > 3 and word in content_lower)
#             score += word_matches
#
#             if score > 0:
#                 scored_docs.append({
#                     'content': doc['content'],
#                     'source': doc['source'],
#                     'section_id': doc['section_id'],
#                     'keywords': doc['keywords'],
#                     'score': score
#                 })
#
#         scored_docs.sort(key=lambda x: x['score'], reverse=True)
#         return scored_docs[:top_k]
#
#     def handle_query(self, question: str) -> str:
#         """Обробка запиту технічним агентом"""
#         relevant_docs = self.search_documents(question)
#
#         if not relevant_docs:
#             return f"{self.agent_name}:\n❌ Не знайшов відповідної інформації в технічній документації. Спробуйте перефразувати запит."
#
#         response = f"{self.agent_name}:\n🔍 **Відповідь на основі технічної документації:**\n\n"
#
#         for i, doc in enumerate(relevant_docs, 1):
#             content_preview = doc['content']
#             if len(content_preview) > 500:
#                 sentences = re.split(r'[.!?]', content_preview)
#                 preview = ""
#                 for sentence in sentences:
#                     if len(preview + sentence) < 500:
#                         preview += sentence + '.'
#                     else:
#                         break
#                 content_preview = preview + "..." if preview else content_preview[:500] + "..."
#
#             response += f"**📚 Джерело {i}: {doc['source']}**\n"
#             response += f"{content_preview}\n\n"
#
#         return response
#
#
# class BillingAgentB:
#     """
#     Агент Б - Спеціаліст з виставлення рахунків
#     Спеціалізація: рахунки, відшкодування, платежі
#     """
#
#     def __init__(self):
#         self.agent_name = "💼 Агент Б (Спеціаліст з рахунків)"
#         self.refund_requests = {}
#         self.invoices = {}
#
#         # Політика відшкодувань
#         self.refund_policy = {
#             "standard": {"days": 14, "fee": 0.0},
#             "premium": {"days": 7, "fee": 0.0},
#             "express": {"days": 3, "fee": 0.1}
#         }
#
#     def handle_query(self, question: str) -> str:
#         """Обробка запиту агентом з рахунків"""
#         question_lower = question.lower()
#
#         # Визначення типу запиту
#         if any(word in question_lower for word in ['відшкодування', 'рефанд', 'повернення', 'refund']):
#             return self.handle_refund_request(question)
#         elif any(word in question_lower for word in ['рахунок', 'інвойс', 'оплата', 'платіж', 'invoice', 'bill']):
#             return self.handle_invoice_request(question)
#         elif any(word in question_lower for word in ['політика', 'умови', 'терміни', 'policy']):
#             return self.explain_refund_policy()
#         elif any(word in question_lower for word in ['статус', 'status', 'перевірити']):
#             return self.check_request_status(question)
#         else:
#             return self.general_billing_response(question)
#
#     def handle_refund_request(self, question: str) -> str:
#         """Обробка запиту на відшкодування"""
#         # Генерація унікального ID запиту
#         request_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
#
#         # Визначення типу відшкодування з питання
#         refund_type = "standard"
#         if "преміум" in question.lower() or "швидкий" in question.lower():
#             refund_type = "premium"
#         elif "експрес" in question.lower() or "терміновий" in question.lower():
#             refund_type = "express"
#
#         # Збереження запиту
#         self.refund_requests[request_id] = {
#             "type": refund_type,
#             "status": "pending_form",
#             "created_at": datetime.now(),
#             "estimated_completion": datetime.now() + timedelta(days=self.refund_policy[refund_type]["days"])
#         }
#
#         response = f"{self.agent_name}:\n✅ **Запит на відшкодування створено!**\n\n"
#         response += f"📋 **Деталі запиту:**\n"
#         response += f"   • Номер запиту: `{request_id}`\n"
#         response += f"   • Тип відшкодування: {refund_type}\n"
#         response += f"   • Очікуваний термін: {self.refund_policy[refund_type]['days']} днів\n"
#
#         if refund_type == "express":
#             response += f"   • Комісія: {self.refund_policy[refund_type]['fee'] * 100}%\n"
#
#         response += f"\n📝 **Наступні кроки:**\n"
#         response += f"1. Заповніть форму для відшкодування за посиланням: https://forms.company/refund/{request_id}\n"
#         response += f"2. Надішліть заповнену форму на email: refunds@company.com\n"
#         response += f"3. Ми зв'яжемося з вами протягом 24 годин\n"
#
#         response += f"\n💡 *Збережіть номер запиту {request_id} для подальшого відстеження статусу*"
#
#         return response
#
#     def handle_invoice_request(self, question: str) -> str:
#         """Обробка запиту щодо рахунків"""
#         invoice_id = f"INV-{uuid.uuid4().hex[:6].upper()}"
#
#         # Аналіз питання для визначення типу рахунку
#         amount = "1000.00"  # Приклад суми
#         if "проформу" in question.lower() or "попередній" in question.lower():
#             invoice_type = "proforma"
#         else:
#             invoice_type = "standard"
#
#         self.invoices[invoice_id] = {
#             "type": invoice_type,
#             "amount": amount,
#             "status": "generated",
#             "created_at": datetime.now()
#         }
#
#         response = f"{self.agent_name}:\n📄 **Рахунок готовий!**\n\n"
#         response += f"**Деталі рахунку:**\n"
#         response += f"   • Номер рахунку: `{invoice_id}`\n"
#         response += f"   • Тип: {invoice_type}\n"
#         response += f"   • Сума: {amount} грн\n"
#         response += f"   • Термін оплати: 30 днів\n"
#
#         response += f"\n**Спосіб оплати:**\n"
#         response += f"1. Електронний платіж: https://pay.company.com/{invoice_id}\n"
#         response += f"2. Банківський переказ: IBAN UA123456789012345678901234567\n"
#         response += f"3. Готівкою в офісі\n"
#
#         response += f"\n📧 Рахунок було відправлено на вашу електронну пошту"
#
#         return response
#
#     def explain_refund_policy(self) -> str:
#         """Пояснення політики відшкодувань"""
#         response = f"{self.agent_name}:\n📋 **Політика відшкодувань**\n\n"
#
#         for policy_type, details in self.refund_policy.items():
#             response += f"**{policy_type.upper()}:**\n"
#             response += f"   • Термін обробки: {details['days']} днів\n"
#             if details['fee'] > 0:
#                 response += f"   • Комісія: {details['fee'] * 100}%\n"
#             response += f"\n"
#
#         response += "**Умови:**\n"
#         response += "• Відшкодування можливе протягом 30 днів з моменту покупки\n"
#         response += "• Товар повинен бути в оригінальному стані\n"
#         response += "• Необхідно надати чек або інший доказ покупки\n"
#
#         return response
#
#     def check_request_status(self, question: str) -> str:
#         """Перевірка статусу запиту"""
#         # Спроба знайти ID у питанні
#         found_id = None
#         for word in question.upper().split():
#             if word.startswith('REF-') and word in self.refund_requests:
#                 found_id = word
#                 break
#             elif word.startswith('INV-') and word in self.invoices:
#                 found_id = word
#
#         if not found_id:
#             return f"{self.agent_name}:\n❌ Не вдалося знайти запит. Будь ласка, надайте номер запиту (REF-XXXXXXX або INV-XXXXXX)"
#
#         if found_id.startswith('REF-'):
#             request = self.refund_requests[found_id]
#             response = f"{self.agent_name}:\n📊 **Статус відшкодування {found_id}**\n\n"
#             response += f"   • Статус: {request['status']}\n"
#             response += f"   • Тип: {request['type']}\n"
#             response += f"   • Створено: {request['created_at'].strftime('%d.%m.%Y')}\n"
#             response += f"   • Очікується завершення: {request['estimated_completion'].strftime('%d.%m.%Y')}\n"
#         else:
#             invoice = self.invoices[found_id]
#             response = f"{self.agent_name}:\n📊 **Статус рахунку {found_id}**\n\n"
#             response += f"   • Статус: {invoice['status']}\n"
#             response += f"   • Сума: {invoice['amount']} грн\n"
#             response += f"   • Створено: {invoice['created_at'].strftime('%d.%m.%Y')}\n"
#
#         return response
#
#     def general_billing_response(self, question: str) -> str:
#         """Загальна відповідь щодо рахунків"""
#         response = f"{self.agent_name}:\n💼 **Спеціаліст з рахунків готовий допомогти!**\n\n"
#         response += "Я можу допомогти з:\n"
#         response += "• 🧾 Виставленням рахунків та інвойсів\n"
#         response += "• 💰 Запитами на відшкодування коштів\n"
#         response += "• 📋 Поясненням політики відшкодувань\n"
#         response += "• 🔍 Перевіркою статусу запитів\n"
#         response += "• 💳 Питаннями щодо оплати\n\n"
#         response += "Будь ласка, уточніть ваш запит для кращої допомоги!"
#
#         return response
#
#
# class AgentDispatcher:
#     """
#     Диспетчер для вибору відповідного агента
#     """
#
#     def __init__(self):
#         self.agent_a = TechnicalAgentA("./docs")
#         self.agent_b = BillingAgentB()
#         self.conversation_history = []
#
#     def classify_intent(self, question: str) -> str:
#         """Класифікація наміру запиту"""
#         question_lower = question.lower()
#
#         # Ключові слова для Агента Б (рахунки)
#         billing_keywords = [
#             'рахунок', 'інвойс', 'оплата', 'платіж', 'відшкодування', 'рефанд',
#             'повернення', 'гроші', 'кошти', 'ціна', 'вартість', 'тариф', 'план',
#             'оплатити', 'заплатити', 'bill', 'invoice', 'payment', 'refund',
#             'money', 'cost', 'price', 'fee', 'комісія', 'перерахування'
#         ]
#
#         # Ключові слова для Агента А (технічні)
#         tech_keywords = [
#              'IP', 'MAC', 'Wi-Fi', 'USB', 'HDMI', 'DNS', 'DHCP', 'NAT', 'TCP', 'UDP',
#             'HTTP', 'HTTPS', 'SSH', 'FTP', 'VPN', 'LAN', 'WAN', 'MAN', 'WLAN',
#             'компьютер', 'ноутбук', 'мережа', 'інтернет', 'wi-fi', 'ip', 'mac',
#             'драйвер', 'програмне', 'апаратне', 'технічний', 'налаштування',
#             'підключення', "з'єднання", 'сервер', 'роутер', 'модем', 'кабель',
#             'computer', 'laptop', 'network', 'internet', 'wifi', 'driver',
#             'software', 'hardware', 'technical', 'setup', 'configure'
#         ]
#
#         billing_score = sum(1 for word in billing_keywords if word in question_lower)
#         tech_score = sum(1 for word in tech_keywords if word in question_lower)
#
#         if billing_score > tech_score:
#             return "billing"
#         elif tech_score > billing_score:
#             return "technical"
#         else:
#             # Якщо рівні, перевіряємо контекст останніх повідомлень
#             if self.conversation_history:
#                 last_agent = self.conversation_history[-1].get('agent')
#                 if last_agent:
#                     return last_agent
#             return "billing"  # За замовчуванням
#
#     def handle_message(self, user_message: str) -> str:
#         """Обробка повідомлення користувача"""
#         if not user_message.strip():
#             return "Будь ласка, введіть ваше питання."
#
#         # Визначення відповідного агента
#         intent = self.classify_intent(user_message)
#
#         if intent == "technical":
#             response = self.agent_a.handle_query(user_message)
#             agent_used = "technical"
#         else:
#             response = self.agent_b.handle_query(user_message)
#             agent_used = "billing"
#
#         # Збереження в історії
#         self.conversation_history.append({
#             "timestamp": datetime.now(),
#             "user_message": user_message,
#             "agent_response": response,
#             "agent": agent_used
#         })
#
#         # Обмеження історії
#         if len(self.conversation_history) > 10:
#             self.conversation_history = self.conversation_history[-10:]
#
#         return response
#
#     def get_conversation_stats(self) -> Dict:
#         """Статистика розмови"""
#         agent_counts = {"technical": 0, "billing": 0}
#         for entry in self.conversation_history:
#             if entry["agent"] in agent_counts:
#                 agent_counts[entry["agent"]] += 1
#
#         return {
#             "total_messages": len(self.conversation_history),
#             "agent_usage": agent_counts,
#             "last_agent": self.conversation_history[-1]["agent"] if self.conversation_history else None
#         }
#
#
# def main():
#     """Головна функція для запуску системи"""
#     print("🚀 Запуск системи з двох агентів...")
#     print("🤖 Агент А - Технічний спеціаліст")
#     print("💼 Агент Б - Спеціаліст з рахунків")
#     print("-" * 50)
#
#     # Ініціалізація диспетчера
#     dispatcher = AgentDispatcher()
#
#     print("\n💬 Система готова до роботи!")
#     print("Доступні команди:")
#     print("  - 'статистика' - показати статистику розмови")
#     print("  - 'історія' - показати останні повідомлення")
#     print("  - 'clear' - очистити історію")
#     print("  - 'quit' - вихід")
#     print("\nЗадавайте ваші питання:")
#
#     while True:
#         try:
#             user_input = input("\n👤 Ваше повідомлення: ").strip()
#
#             if user_input.lower() in ['quit', 'exit', 'вихід']:
#                 print("👋 До побачення!")
#                 break
#
#             if not user_input:
#                 continue
#
#             # Обробка спеціальних команд
#             if user_input.lower() == 'статистика':
#                 stats = dispatcher.get_conversation_stats()
#                 print(f"\n📊 Статистика розмови:")
#                 print(f"   • Всього повідомлень: {stats['total_messages']}")
#                 print(f"   • Використано Агента А: {stats['agent_usage']['technical']}")
#                 print(f"   • Використано Агента Б: {stats['agent_usage']['billing']}")
#                 print(f"   • Останній агент: {stats['last_agent']}")
#                 continue
#
#             elif user_input.lower() == 'історія':
#                 print(f"\n📜 Останні повідомлення:")
#                 for i, entry in enumerate(dispatcher.conversation_history[-5:], 1):
#                     print(f"\n{i}. [{entry['timestamp'].strftime('%H:%M')}] {entry['user_message'][:50]}...")
#                     print(f"   → Агент: {entry['agent']}")
#                 continue
#
#             elif user_input.lower() == 'clear':
#                 dispatcher.conversation_history = []
#                 print("🗑️ Історія очищена!")
#                 continue
#
#             # Обробка звичайного повідомлення
#             response = dispatcher.handle_message(user_input)
#             print(f"\n{response}")
#
#         except KeyboardInterrupt:
#             print("\n👋 До побачення!")
#             break
#         except Exception as e:
#             print(f"\n❌ Сталася помилка: {e}")
#
#
# if __name__ == "__main__":
#     # Створення необхідних директорій
#     docs_dir = Path("./docs")
#     docs_dir.mkdir(exist_ok=True)
#
#     print("📁 Система автоматично використовує папку './docs' для технічної документації")
#
#     # Перевірка наявності файлів
#     existing_files = list(docs_dir.glob("*.txt"))
#     if existing_files:
#         print(f"📋 Знайдено технічних документів: {len(existing_files)}")
#     else:
#         print("⚠️ Технічних документів не знайдено. Агент А буде обмежений у відповідях.")
#


import os
import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import uuid
from openai import OpenAI


class OpenAIClient:
    """Клієнт для роботи з OpenAI API"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY не знайдено. Встановіть змінну середовища або передайте ключ напряму.")

        self.client = OpenAI(api_key=self.api_key)

    def generate_response(self, messages: List[Dict], model: str = "gpt-3.5-turbo",
                          temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Генерація відповіді через OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Помилка з'єднання з ChatGPT: {str(e)}"


class TechnicalAgentA:
    """
    Агент А - Технічний спеціаліст з інтеграцією ChatGPT
    """

    def __init__(self, docs_directory: str = "./docs", openai_client: OpenAIClient = None):
        self.docs_directory = Path(docs_directory)
        self.documents = []
        self.openai_client = openai_client
        self.agent_name = "🤖 Агент А (Технічний спеціаліст)"

        self.load_documents()

    def load_documents(self):
        """Завантаження технічних документів"""
        text_files = list(self.docs_directory.glob("*.txt"))
        for file_path in text_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                self.process_document(content, file_path.name)
            except Exception as e:
                print(f"❌ Помилка завантаження {file_path}: {e}")

    def process_document(self, content: str, source: str):
        """Обробка документів"""
        sections = re.split(r'\n\s*\n', content)
        for i, section in enumerate(sections):
            if len(section.strip()) > 50:
                self.documents.append({
                    'content': section.strip(),
                    'source': source,
                    'section_id': i + 1
                })

    def search_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Пошук релевантних документів"""
        if not self.documents:
            return []

        query_lower = query.lower()
        scored_docs = []

        for doc in self.documents:
            score = 0
            content_lower = doc['content'].lower()

            if query_lower in content_lower:
                score += 5

            query_words = query_lower.split()
            word_matches = sum(1 for word in query_words if len(word) > 3 and word in content_lower)
            score += word_matches

            if score > 0:
                scored_docs.append({
                    'content': doc['content'],
                    'source': doc['source'],
                    'section_id': doc['section_id'],
                    'score': score
                })

        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        return scored_docs[:top_k]

    def handle_query(self, question: str) -> str:
        """Обробка запиту з використанням ChatGPT"""
        relevant_docs = self.search_documents(question)

        if not relevant_docs and not self.openai_client:
            return f"{self.agent_name}:\n❌ Не знайшов відповідної інформації в технічній документації."

        if not self.openai_client:
            # Резервна відповідь без ChatGPT
            response = f"{self.agent_name}:\n🔍 **Відповідь на основі технічної документації:**\n\n"
            for doc in relevant_docs:
                response += f"**{doc['source']}:** {doc['content'][:300]}...\n\n"
            return response

        # Формуємо контекст для ChatGPT
        context = "Технічна документація:\n"
        for doc in relevant_docs:
            context += f"\n--- {doc['source']} ---\n{doc['content']}\n"

        messages = [
            {
                "role": "system",
                "content": """Ти - технічний спеціаліст з комп'ютерної техніки та мереж. 
                Відповідай ВИКЛЮЧНО на основі наданої технічної документації. 
                Якщо інформації недостатньо - скажи про це. 
                Будь точним та технічним. Відповідай українською мовою."""
            },
            {
                "role": "user",
                "content": f"Контекст:\n{context}\n\nПитання: {question}"
            }
        ]

        gpt_response = self.openai_client.generate_response(messages, temperature=0.3)

        response = f"{self.agent_name}:\n🤖 **Відповідь з використанням AI:**\n\n{gpt_response}"

        if relevant_docs:
            response += f"\n\n📚 **Використані джерела:**"
            for doc in relevant_docs:
                response += f"\n• {doc['source']} (розділ {doc['section_id']})"

        return response


class BillingAgentB:
    """
    Агент Б - Спеціаліст з виставлення рахунків з інтеграцією ChatGPT
    """

    def __init__(self, openai_client: OpenAIClient = None):
        self.agent_name = "💼 Агент Б (Спеціаліст з рахунків)"
        self.openai_client = openai_client
        self.refund_requests = {}
        self.invoices = {}

        # Політика відшкодувань
        self.refund_policy = {
            "standard": {"days": 14, "fee": 0.0, "description": "Стандартне відшкодування"},
            "premium": {"days": 7, "fee": 0.0, "description": "Преміум відшкодування"},
            "express": {"days": 3, "fee": 0.1, "description": "Експрес відшкодування (комісія 10%)"}
        }

    def handle_query(self, question: str) -> str:
        """Обробка запиту з використанням ChatGPT"""
        question_lower = question.lower()

        # Спочатку спробуємо обробити структурованими методами
        structured_response = self._try_structured_handling(question)
        if structured_response:
            return structured_response

        # Якщо структурована обробка не вдалась, використовуємо ChatGPT
        if self.openai_client:
            return self._handle_with_chatgpt(question)
        else:
            return self._fallback_response(question)

    def _try_structured_handling(self, question: str) -> Optional[str]:
        """Спробувати обробити запит структурованими методами"""
        question_lower = question.lower()

        if any(word in question_lower for word in ['відшкодування', 'рефанд', 'повернення', 'refund']):
            return self.handle_refund_request(question)
        elif any(word in question_lower for word in ['рахунок', 'інвойс', 'invoice', 'bill']):
            return self.handle_invoice_request(question)
        elif any(word in question_lower for word in ['політика', 'умови', 'терміни', 'policy']):
            return self.explain_refund_policy()
        elif any(word in question_lower for word in ['статус', 'status', 'перевірити']):
            return self.check_request_status(question)

        return None

    def _handle_with_chatgpt(self, question: str) -> str:
        """Обробка запиту за допомогою ChatGPT"""
        # Контекст для ChatGPT
        context = {
            "refund_policy": self.refund_policy,
            "active_requests": list(self.refund_requests.keys()),
            "active_invoices": list(self.invoices.keys())
        }

        messages = [
            {
                "role": "system",
                "content": """Ти - фахівець з виставлення рахунків та відшкодувань. 
                Твої можливості:
                1. Створення запитів на відшкодування
                2. Генерація рахунків/інвойсів
                3. Пояснення політики відшкодувань
                4. Перевірка статусу запитів
                5. Відповіді на питання щодо оплати та рахунків

                Політика відшкодувань:
                - Стандартне: 14 днів, без комісії
                - Преміум: 7 днів, без комісії  
                - Експрес: 3 дні, комісія 10%

                Будь точним, професійним та корисним. Відповідай українською мовою."""
            },
            {
                "role": "user",
                "content": f"Контекст: {json.dumps(context, ensure_ascii=False)}\n\nПитання: {question}"
            }
        ]

        gpt_response = self.openai_client.generate_response(messages, temperature=0.5)

        # Додаємо структуровану інформацію до відповіді GPT
        response = f"{self.agent_name}:\n🤖 **Відповідь з використанням AI:**\n\n{gpt_response}"

        # Додаємо корисні посилання, якщо це доречно
        if any(word in question.lower() for word in ['відшкодування', 'рефанд']):
            response += f"\n\n💡 **Швидкі дії:**\n"
            response += f"• Створити запит на відшкодування: напишіть 'відшкодування'\n"
            response += f"• Дізнатись політику: напишіть 'політика відшкодувань'"

        return response

    def _fallback_response(self, question: str) -> str:
        """Резервна відповідь без ChatGPT"""
        response = f"{self.agent_name}:\n💼 **Спеціаліст з рахунків**\n\n"
        response += "Я можу допомогти з:\n"
        response += "• 🧾 Виставленням рахунків (напишіть 'рахунок')\n"
        response += "• 💰 Відшкодуваннями (напишіть 'відшкодування')\n"
        response += "• 📋 Політикою відшкодувань (напишіть 'політика')\n"
        response += "• 🔍 Перевіркою статусу (напишіть 'статус')\n\n"
        response += "Будь ласка, уточніть ваш запит!"

        return response

    def handle_refund_request(self, question: str) -> str:
        """Обробка запиту на відшкодування"""
        request_id = f"REF-{uuid.uuid4().hex[:8].upper()}"

        refund_type = "standard"
        if "преміум" in question.lower():
            refund_type = "premium"
        elif "експрес" in question.lower() or "терміново" in question.lower():
            refund_type = "express"

        self.refund_requests[request_id] = {
            "type": refund_type,
            "status": "pending_form",
            "created_at": datetime.now(),
            "estimated_completion": datetime.now() + timedelta(days=self.refund_policy[refund_type]["days"])
        }

        response = f"{self.agent_name}:\n✅ **Запит на відшкодування створено!**\n\n"
        response += f"📋 **Деталі запиту {request_id}:**\n"
        response += f"   • Тип: {self.refund_policy[refund_type]['description']}\n"
        response += f"   • Термін обробки: {self.refund_policy[refund_type]['days']} днів\n"

        if self.refund_policy[refund_type]['fee'] > 0:
            response += f"   • Комісія: {self.refund_policy[refund_type]['fee'] * 100}%\n"

        response += f"\n📝 **Наступні кроки:**\n"
        response += f"1. Заповніть форму: https://forms.company/refund/{request_id}\n"
        response += f"2. Надішліть на refunds@company.com\n"
        response += f"3. Статус: /status {request_id}\n"

        return response

    def handle_invoice_request(self, question: str) -> str:
        """Обробка запиту щодо рахунків"""
        invoice_id = f"INV-{uuid.uuid4().hex[:6].upper()}"

        amount = "1,000.00"
        if "сума" in question.lower():
            # Спроба витягнути суму з питання
            amount_match = re.search(r'(\d+[,\d]*)', question)
            if amount_match:
                amount = amount_match.group(1)

        self.invoices[invoice_id] = {
            "type": "standard",
            "amount": amount,
            "status": "generated",
            "created_at": datetime.now()
        }

        response = f"{self.agent_name}:\n📄 **Рахунок {invoice_id} готовий!**\n\n"
        response += f"**Деталі:**\n"
        response += f"   • Сума: {amount} грн\n"
        response += f"   • Термін оплати: 30 днів\n"
        response += f"   • Статус: згенеровано\n"

        response += f"\n**Оплата:**\n"
        response += f"• Онлайн: https://pay.company.com/{invoice_id}\n"
        response += f"• Банк: IBAN UA12 3456 7890 1234 5678 9012 345\n"
        response += f"• Готівка: в офісі компанії\n"

        return response

    def explain_refund_policy(self) -> str:
        """Пояснення політики відшкодувань"""
        response = f"{self.agent_name}:\n📋 **Політика відшкодувань**\n\n"

        for policy_type, details in self.refund_policy.items():
            response += f"**{details['description']}:**\n"
            response += f"   ⏱️ Термін: {details['days']} днів\n"
            if details['fee'] > 0:
                response += f"   💰 Комісія: {details['fee'] * 100}%\n"
            response += f"\n"

        response += "**Загальні умови:**\n"
        response += "• Максимальний термін - 30 днів з покупки\n"
        response += "• Товар у оригінальному стані\n"
        response += "• Наявність чека/підтвердження\n"
        response += "• Для послуг - не більше 50% виконаної роботи\n"

        return response

    def check_request_status(self, question: str) -> str:
        """Перевірка статусу запиту"""
        found_id = None
        for word in question.upper().split():
            if word.startswith('REF-') and word in self.refund_requests:
                found_id = word
                break
            elif word.startswith('INV-') and word in self.invoices:
                found_id = word

        if not found_id:
            return f"{self.agent_name}:\n❌ Запит не знайдено. Надайте номер (REF-... або INV-...)"

        if found_id.startswith('REF-'):
            request = self.refund_requests[found_id]
            response = f"{self.agent_name}:\n📊 **Статус відшкодування {found_id}**\n\n"
            response += f"   • Статус: {request['status']}\n"
            response += f"   • Тип: {self.refund_policy[request['type']]['description']}\n"
            response += f"   • Створено: {request['created_at'].strftime('%d.%m.%Y')}\n"
            response += f"   • Завершення: {request['estimated_completion'].strftime('%d.%m.%Y')}\n"
        else:
            invoice = self.invoices[found_id]
            response = f"{self.agent_name}:\n📊 **Статус рахунку {found_id}**\n\n"
            response += f"   • Статус: {invoice['status']}\n"
            response += f"   • Сума: {invoice['amount']} грн\n"
            response += f"   • Створено: {invoice['created_at'].strftime('%d.%m.%Y')}\n"

        return response


class AgentDispatcher:
    """
    Диспетчер з інтелектуальним вибором агента
    """

    def __init__(self, openai_client: OpenAIClient = None):
        self.agent_a = TechnicalAgentA("./docs", openai_client)
        self.agent_b = BillingAgentB(openai_client)
        self.openai_client = openai_client
        self.conversation_history = []

    def classify_intent(self, question: str) -> Tuple[str, float]:
        """Класифікація наміру з використанням ChatGPT або ключових слів"""

        # Список ключових слів для кожного агента
        billing_keywords = [
            'рахунок', 'інвойс', 'оплата', 'платіж', 'відшкодування', 'рефанд',
            'повернення', 'гроші', 'кошти', 'ціна', 'вартість', 'тариф', 'план',
            'оплатити', 'заплатити', 'bill', 'invoice', 'payment', 'refund',
            'money', 'cost', 'price', 'fee', 'комісія', 'перерахування'
        ]

        tech_keywords = [
            'компьютер', 'ноутбук', 'мережа', 'інтернет', 'wi-fi', 'ip', 'mac',
            'драйвер', 'програмне', 'апаратне', 'технічний', 'налаштування',
            'підключення', 'з\'єднання', 'сервер', 'роутер', 'модем', 'кабель',
            'computer', 'laptop', 'network', 'internet', 'wifi', 'driver',
            'software', 'hardware', 'technical', 'setup', 'configure'
        ]

        question_lower = question.lower()

        billing_score = sum(1 for word in billing_keywords if word in question_lower)
        tech_score = sum(1 for word in tech_keywords if word in question_lower)

        # Якщо є явний переможець
        if billing_score > tech_score * 2:
            return "billing", 0.9
        elif tech_score > billing_score * 2:
            return "technical", 0.9

        # Якщо ChatGPT доступний, використовуємо його для точнішої класифікації
        if self.openai_client and (billing_score > 0 or tech_score > 0):
            return self._classify_with_chatgpt(question)

        # За замовчуванням або за контекстом
        if self.conversation_history:
            last_agent = self.conversation_history[-1].get('agent')
            if last_agent:
                return last_agent, 0.7

        return "billing", 0.5  # За замовчуванням

    def _classify_with_chatgpt(self, question: str) -> Tuple[str, float]:
        """Класифікація за допомогою ChatGPT"""
        messages = [
            {
                "role": "system",
                "content": """Ти класифікуєш запити між двома агентами:
                1. Технічний спеціаліст (technical) - питання про комп'ютери, мережі, техніку
                2. Спеціаліст з рахунків (billing) - питання про оплату, рахунки, відшкодування

                Відповідай ТІЛЬКИ одним словом: 'technical' або 'billing'"""
            },
            {
                "role": "user",
                "content": f"Запит: {question}"
            }
        ]

        try:
            response = self.openai_client.generate_response(messages, temperature=0.1, max_tokens=10)
            intent = response.strip().lower()

            if intent in ['technical', 'billing']:
                return intent, 0.95
        except:
            pass

        return "billing", 0.5

    def handle_message(self, user_message: str) -> str:
        """Обробка повідомлення користувача"""
        if not user_message.strip():
            return "Будь ласка, введіть ваше питання."

        # Визначення відповідного агента
        intent, confidence = self.classify_intent(user_message)

        if confidence < 0.6:
            # Низька впевненість - запитуємо уточнення
            response = "❓ **Уточніть, будь ласка:**\n\n"
            response += "🤖 **Технічні питання** (комп'ютери, мережі, техніка)\n"
            response += "💼 **Фінансові питання** (рахунки, оплата, відшкодування)\n\n"
            response += "Що вас цікавить?"
            return response

        if intent == "technical":
            response = self.agent_a.handle_query(user_message)
            agent_used = "technical"
        else:
            response = self.agent_b.handle_query(user_message)
            agent_used = "billing"

        # Збереження в історії
        self.conversation_history.append({
            "timestamp": datetime.now(),
            "user_message": user_message,
            "agent_response": response,
            "agent": agent_used,
            "confidence": confidence
        })

        # Обмеження історії
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

        return response

    def get_conversation_stats(self) -> Dict:
        """Статистика розмови"""
        agent_counts = {"technical": 0, "billing": 0}
        for entry in self.conversation_history:
            if entry["agent"] in agent_counts:
                agent_counts[entry["agent"]] += 1

        return {
            "total_messages": len(self.conversation_history),
            "agent_usage": agent_counts,
            "last_agent": self.conversation_history[-1]["agent"] if self.conversation_history else None,
            "openai_available": self.openai_client is not None
        }


def main():
    """Головна функція для запуску системи"""
    print("🚀 Запуск системи з інтеграцією ChatGPT...")
    print("🤖 Агент А - Технічний спеціаліст")
    print("💼 Агент Б - Спеціаліст з рахунків")
    print("-" * 50)

    # Перевірка API ключа
    api_key = os.getenv('OPENAI_API_KEY')
    openai_client = None

    if api_key:
        try:
            openai_client = OpenAIClient(api_key)
            print("✅ ChatGPT інтегрований у систему")
        except Exception as e:
            print(f"❌ Помилка ініціалізації ChatGPT: {e}")
            print("⚠️  Система працюватиме в обмеженому режимі")
    else:
        print("⚠️  OPENAI_API_KEY не знайдено. Система працюватиме в обмеженому режимі")

    # Ініціалізація диспетчера
    dispatcher = AgentDispatcher(openai_client)

    print("\n💬 Система готова до роботи!")
    print("Доступні команди:")
    print("  - 'статистика' - показати статистику розмови")
    print("  - 'історія' - показати останні повідомлення")
    print("  - 'clear' - очистити історію")
    print("  - 'quit' - вихід")
    print("\nЗадавайте ваші питання:")

    while True:
        try:
            user_input = input("\n👤 Ваше повідомлення: ").strip()

            if user_input.lower() in ['quit', 'exit', 'вихід']:
                print("👋 До побачення!")
                break

            if not user_input:
                continue

            # Обробка спеціальних команд
            if user_input.lower() == 'статистика':
                stats = dispatcher.get_conversation_stats()
                print(f"\n📊 Статистика розмови:")
                print(f"   • Всього повідомлень: {stats['total_messages']}")
                print(f"   • Агент А (тех.): {stats['agent_usage']['technical']}")
                print(f"   • Агент Б (фін.): {stats['agent_usage']['billing']}")
                print(f"   • ChatGPT: {'✅' if stats['openai_available'] else '❌'}")
                continue

            elif user_input.lower() == 'історія':
                print(f"\n📜 Останні повідомлення:")
                for i, entry in enumerate(dispatcher.conversation_history[-5:], 1):
                    print(f"\n{i}. [{entry['timestamp'].strftime('%H:%M')}] {entry['user_message'][:50]}...")
                    print(f"   → Агент: {entry['agent']} (впевненість: {entry.get('confidence', 0):.2f})")
                continue

            elif user_input.lower() == 'clear':
                dispatcher.conversation_history = []
                print("🗑️ Історія очищена!")
                continue

            # Обробка звичайного повідомлення
            response = dispatcher.handle_message(user_input)
            print(f"\n{response}")

        except KeyboardInterrupt:
            print("\n👋 До побачення!")
            break
        except Exception as e:
            print(f"\n❌ Сталася помилка: {e}")


if __name__ == "__main__":
    # Створення необхідних директорій
    docs_dir = Path("./docs")
    docs_dir.mkdir(exist_ok=True)

    print("📁 Система автоматично використовує папку './docs' для технічної документації")

    # Перевірка наявності файлів
    existing_files = list(docs_dir.glob("*.txt"))
    if existing_files:
        print(f"📋 Знайдено технічних документів: {len(existing_files)}")
    else:
        print("⚠️ Технічних документів не знайдено. Агент А буде обмежений у відповідях.")

    main()