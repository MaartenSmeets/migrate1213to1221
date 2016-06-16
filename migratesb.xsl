<xsl:stylesheet
    version="1.0"
    xmlns:src="http://maven.apache.org/POM/4.0.0" 
    xmlns="http://maven.apache.org/POM/4.0.0"   
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:namespace-alias stylesheet-prefix="src" result-prefix=""/>
<!--
	if you want to remove the parent
	<xsl:template match="/src:project/src:parent"/>
-->
	
	<xsl:template match="/src:project/src:groupId">
		<src:groupId>
			<xsl:call-template name="string-replace-all">
				<xsl:with-param name="text" select="." />
				<xsl:with-param name="replace" select="'oldgroupid'" />
				<xsl:with-param name="by" select="'newgroupid'" />
			</xsl:call-template>
		</src:groupId>
	</xsl:template>
<!--
	if you want to change the packaging
	<xsl:template match="/src:project/src:packaging[text()='sbar']">
		<src:packaging>jar</src:packaging>
	</xsl:template>
-->
	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>

	<xsl:template name="string-replace-all">
		<xsl:param name="text" />
		<xsl:param name="replace" />
		<xsl:param name="by" />
		<xsl:choose>
			<xsl:when test="$text = '' or $replace = ''or not($replace)" >
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
