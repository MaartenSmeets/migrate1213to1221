<xsl:stylesheet
    version="1.0"
    xmlns:src="http://maven.apache.org/POM/4.0.0" 
    xmlns="http://maven.apache.org/POM/4.0.0"   
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:namespace-alias stylesheet-prefix="src" result-prefix=""/>

	<xsl:template match="/src:project/src:parent/src:version">
		<src:version>12.2.1-0-0</src:version>
	</xsl:template>

	<xsl:template match="/src:project/src:groupId">
		<src:groupId>
			<xsl:call-template name="string-replace-all">
				<xsl:with-param name="text" select="." />
				<xsl:with-param name="replace" select="'oldgroupid'" />
				<xsl:with-param name="by" select="'newgroupid'" />
			</xsl:call-template>
		</src:groupId>
	</xsl:template>

	<xsl:template match="/src:project/src:build/src:plugins/src:plugin[src:groupId='com.oracle.soa.plugin']/src:version">
		<src:version>12.2.1-0-0</src:version>
	</xsl:template>

	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>
<!-- below for Java embedding in BPEL processes -->
	<xsl:template match="/src:project/src:build/src:plugins/src:plugin[src:groupId='com.oracle.soa.plugin']">
		<xsl:copy>
			<xsl:apply-templates select="node()|@*"/>
			<xsl:if test="not(src:dependencies)">
				<dependencies>
					<dependency>
						<groupId>javax.el</groupId>
						<artifactId>javax.el-api</artifactId>
						<version>3.0.0</version>
					</dependency>
				</dependencies>
			</xsl:if>
		</xsl:copy>
	</xsl:template>

	<xsl:template name="string-replace-all">
		<xsl:param name="text" />
		<xsl:param name="replace" />
		<xsl:param name="by" />
		<xsl:choose>
			<xsl:when test="$text = '' or $replace = ''or not($replace)" >
				<!-- Prevent this routine from hanging -->
				<xsl:value-of select="$text" />
			</xsl:when>
			<xsl:when test="contains($text, $replace)">
				<xsl:value-of select="substring-before($text,$replace)" />
				<xsl:value-of select="$by" />
				<xsl:call-template name="string-replace-all">
					<xsl:with-param name="text" select="substring-after($text,$replace)" />
					<xsl:with-param name="replace" select="$replace" />
					<xsl:with-param name="by" select="$by" />
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$text" />
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

</xsl:stylesheet>