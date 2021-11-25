FROM rasa/rasa-sdk:2.8.2

COPY actions /app/actions
COPY data /app/data
COPY knowledge_base /app/knowledge_base

USER root
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/actions/requirements.txt

RUN useradd -ms /bin/bash admin
RUN chown -R admin:admin /app
RUN chmod 755 /app
USER admin
CMD ["start", "--actions", "actions"]